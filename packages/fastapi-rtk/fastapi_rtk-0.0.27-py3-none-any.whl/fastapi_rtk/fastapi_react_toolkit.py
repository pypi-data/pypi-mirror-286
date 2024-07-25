import io
import json
import os
from contextlib import asynccontextmanager
from typing import Awaitable, Callable, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_users.exceptions import UserNotExists
from jinja2 import Environment, TemplateNotFound, select_autoescape
from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.routing import _DefaultLifespan

from .auth import AuthDict, CookieConfig, JWTStrategyConfig
from .const import (
    COOKIE_CONFIG_KEYS,
    COOKIE_STRATEGY_KEYS,
    DEFAULT_STATIC_FOLDER,
    DEFAULT_TEMPLATE_FOLDER,
    JWT_STRATEGY_KEYS,
    ROLE_KEYS,
    logger,
)
from .db import UserDatabase, session_manager
from .globals import GlobalsMiddleware, g
from .models import Api, Permission, PermissionApi, Role, User
from .schemas import RoleSchema, UserCreate, UserReadWithPassword
from .utils import ignore_in_migrate, safe_call
from .version import __version__

__all__ = ["FastAPIReactToolkit"]


class FastAPIReactToolkit:
    """
    The main class for the `FastAPIReactToolkit` library.

    This class provides a set of methods to initialize a FastAPI application, add APIs, manage permissions and roles,
    and initialize the database with permissions, APIs, roles, and their relationships.

    Args:
        `app` (FastAPI | None, optional): The FastAPI application instance. If set, the `initialize` method will be called with this instance. Defaults to None.
        `auth` (AuthDict | None, optional): The authentication configuration. Set this if you want to customize the authentication system. See the `AuthDict` type for more details. Defaults to None.
        `create_tables` (bool, optional): Whether to create tables in the database. Not needed if you use a migration system like Alembic. Defaults to False.
        `on_startup` (Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]], optional): Function to call when the app is starting up. Defaults to None.
        `on_shutdown` (Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]], optional): Function to call when the app is shutting down. Defaults to None.

    ## Example:

    ```python
    import logging

    from fastapi import FastAPI, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi_rtk import FastAPIReactToolkit, User
    from fastapi_rtk.manager import UserManager

    from .base_data import add_base_data

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.INFO)


    class CustomUserManager(UserManager):
        async def on_after_login(
            self,
            user: User,
            request: Request | None = None,
            response: Response | None = None,
        ) -> None:
            await super().on_after_login(user, request, response)
            print("User logged in: ", user)


    async def on_startup(app: FastAPI):
        await add_base_data()
        print("base data added")
        pass


    app = FastAPI(docs_url="/openapi/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:6006"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    toolkit = FastAPIReactToolkit(
        auth={
            "user_manager": CustomUserManager,
            # "password_helper": FABPasswordHelper(),  #! Add this line to use old password hash
        },
        create_tables=True,
        on_startup=on_startup,
    )
    toolkit.config.from_pyfile("./app/config.py")
    toolkit.initialize(app)

    from .apis import *

    toolkit.mount()
    ```
    """

    app: FastAPI = None
    apis: list = None
    initialized: bool = False
    create_tables: bool = False
    on_startup: (
        Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]] | None
    ) = None
    on_shutdown: (
        Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]] | None
    ) = None
    _mounted = False

    def __init__(
        self,
        *,
        app: FastAPI | None = None,
        auth: AuthDict | None = None,
        create_tables: bool = False,
        on_startup: (
            Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]] | None
        ) = None,
        on_shutdown: (
            Callable[[FastAPI], None] | Awaitable[Callable[[FastAPI], None]] | None
        ) = None,
    ) -> None:
        g.current_app = self
        g.config.add_callback(self._init_config)
        self.apis = []
        self.create_tables = create_tables
        self.on_startup = on_startup
        self.on_shutdown = on_shutdown

        if auth:
            for key, value in auth.items():
                setattr(g.auth, key, value)

        if app:
            self.initialize(app)

    @ignore_in_migrate
    def initialize(self, app: FastAPI) -> None:
        """
        Initializes the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.

        Returns:
            None
        """
        if self.initialized:
            return

        self.initialized = True
        self.app = app

        from .dependencies import set_global_user

        # Initialize the lifespan
        self._init_lifespan()

        # Add the GlobalsMiddleware
        self.app.add_middleware(GlobalsMiddleware)
        self.app.router.dependencies.append(Depends(set_global_user))

        # Add the APIs
        self._init_basic_apis()

        # Add the JS manifest route
        self._init_js_manifest()

    def add_api(self, api) -> None:
        """
        Adds the specified API to the FastAPI application.

        Parameters:
        - api (ModelRestApi): The API to be added.

        Returns:
        - None

        Raises:
        - ValueError: If the API is added after the `mount()` method is called.
        """
        if self._mounted:
            raise ValueError(
                "API Mounted after mount() was called, please add APIs before calling mount()"
            )

        from .api import ModelRestApi

        api = api if isinstance(api, ModelRestApi) else api()
        self.apis.append(api)
        api.integrate_router(self.app)
        api.toolkit = self

    def total_permissions(self) -> list[str]:
        """
        Returns the total list of permissions required by all APIs.

        Returns:
        - list[str]: The total list of permissions.
        """
        permissions = []
        for api in self.apis:
            permissions.extend(getattr(api, "permissions", []))
        return list(set(permissions))

    @ignore_in_migrate
    def mount(self):
        """
        Mounts the static and template folders specified in the configuration.

        PLEASE ONLY RUN THIS AFTER ALL APIS HAVE BEEN ADDED.
        """
        if self._mounted:
            return

        self._mounted = True
        self._mount_static_folder()
        self._mount_template_folder()

    @ignore_in_migrate
    def connect_to_database(self):
        """
        Connects to the database using the configured SQLAlchemy database URI.

        This method initializes the database session maker with the SQLAlchemy
        database URI specified in the configuration.

        Raises:
            ValueError: If the `SQLALCHEMY_DATABASE_URI` is not set in the configuration.
        """
        uri = g.config.get("SQLALCHEMY_DATABASE_URI")
        if not uri:
            raise ValueError("SQLALCHEMY_DATABASE_URI is not set in the configuration")

        binds = g.config.get("SQLALCHEMY_BINDS")
        session_manager.init_db(uri, binds)
        logger.info("Connected to database")
        logger.info(f"URI: {uri}")
        logger.info(f"Binds: {binds}")

    @ignore_in_migrate
    async def init_database(self):
        """
        Initializes the database by inserting permissions, APIs, roles, and their relationships.

        The initialization process is as follows:
        1. Inserts permissions into the database.
        2. Inserts APIs into the database.
        3. Inserts roles into the database.
        4. Inserts the relationship between permissions and APIs into the database.
        5. Inserts the relationship between permissions, APIs, and roles into the database.

        Returns:
            None
        """
        async with session_manager.session() as db:
            logger.info("INITIALIZING DATABASE")
            await self._insert_permissions(db)
            await self._insert_apis(db)
            await self._insert_roles(db)
            await self._associate_permission_with_api(db)
            await self._associate_permission_api_with_role(db)
            logger.info("DATABASE INITIALIZED")

    async def _insert_permissions(self, db: AsyncSession | Session):
        new_permissions = self.total_permissions()
        stmt = select(Permission).where(Permission.name.in_(new_permissions))
        result = await safe_call(db.scalars(stmt))
        existing_permissions = [permission.name for permission in result.all()]
        if len(new_permissions) == len(existing_permissions):
            return

        permission_objs = [
            Permission(name=permission)
            for permission in new_permissions
            if permission not in existing_permissions
        ]
        for permission in permission_objs:
            logger.info(f"ADDING PERMISSION {permission}")
            db.add(permission)
        await safe_call(db.commit())

    async def _insert_apis(self, db: AsyncSession | Session):
        new_apis = [api.__class__.__name__ for api in self.apis]
        stmt = select(Api).where(Api.name.in_(new_apis))
        result = await safe_call(db.scalars(stmt))
        existing_apis = [api.name for api in result.all()]
        if len(new_apis) == len(existing_apis):
            return

        api_objs = [Api(name=api) for api in new_apis if api not in existing_apis]
        for api in api_objs:
            logger.info(f"ADDING API {api}")
            db.add(api)
        await safe_call(db.commit())

    async def _insert_roles(self, db: AsyncSession | Session):
        new_roles = [g.admin_role, g.public_role]
        stmt = select(Role).where(Role.name.in_(new_roles))
        result = await safe_call(db.scalars(stmt))
        existing_roles = [role.name for role in result.all()]
        if len(new_roles) == len(existing_roles):
            return

        role_objs = [
            Role(name=role) for role in new_roles if role not in existing_roles
        ]
        for role in role_objs:
            logger.info(f"ADDING ROLE {role}")
            db.add(role)
        await safe_call(db.commit())

    async def _associate_permission_with_api(self, db: AsyncSession | Session):
        for api in self.apis:
            new_permissions = getattr(api, "permissions", [])
            if not new_permissions:
                continue

            # Get the api object
            api_stmt = select(Api).where(Api.name == api.__class__.__name__)
            api_obj = await safe_call(db.scalar(api_stmt))

            if not api_obj:
                raise ValueError(f"API {api.__class__.__name__} not found")

            permission_stmt = select(Permission).where(
                and_(
                    Permission.name.in_(new_permissions),
                    ~Permission.id.in_([p.permission_id for p in api_obj.permissions]),
                )
            )
            permission_result = await safe_call(db.scalars(permission_stmt))
            new_permissions = permission_result.all()

            if not new_permissions:
                continue

            for permission in new_permissions:
                permission_api_stmt = insert(PermissionApi).values(
                    permission_id=permission.id, api_id=api_obj.id
                )
                await safe_call(db.execute(permission_api_stmt))
                logger.info(f"ASSOCIATING PERMISSION {permission} WITH API {api_obj}")
            await safe_call(db.commit())

    async def _associate_permission_api_with_role(self, db: AsyncSession | Session):
        # Read config based roles
        roles_dict = g.config.get("ROLES") or g.config.get("FAB_ROLES", {})
        admin_ignored_apis: list[str] = []

        for role_name, role_permissions in roles_dict.items():
            role_stmt = select(Role).where(Role.name == role_name)
            role_result = await safe_call(db.scalars(role_stmt))
            role = role_result.first()
            if not role:
                role = Role(name=role_name)
                logger.info(f"ADDING ROLE {role}")
                db.add(role)

            for api_name, permission_name in role_permissions:
                admin_ignored_apis.append(api_name)
                permission_api_stmt = (
                    select(PermissionApi)
                    .where(
                        and_(Api.name == api_name, Permission.name == permission_name)
                    )
                    .join(Permission)
                    .join(Api)
                )
                permission_api = await safe_call(db.scalar(permission_api_stmt))
                if not permission_api:
                    permission_stmt = select(Permission).where(
                        Permission.name == permission_name
                    )
                    permission = await safe_call(db.scalar(permission_stmt))
                    if not permission:
                        permission = Permission(name=permission_name)
                        logger.info(f"ADDING PERMISSION {permission}")
                        db.add(permission)

                    stmt = select(Api).where(Api.name == api_name)
                    api = await safe_call(db.scalar(stmt))
                    if not api:
                        api = Api(name=api_name)
                        logger.info(f"ADDING API {api}")
                        db.add(api)

                    permission_api = PermissionApi(permission=permission, api=api)
                    logger.info(f"ADDING PERMISSION-API {permission_api}")
                    db.add(permission_api)

                # Associate role with permission-api
                if role not in permission_api.roles:
                    permission_api.roles.append(role)
                    logger.info(
                        f"ASSOCIATING {role} WITH PERMISSION-API {permission_api}"
                    )

                await safe_call(db.commit())

        # Get admin role
        admin_role_stmt = select(Role).where(Role.name == g.admin_role)
        admin_role = await safe_call(db.scalar(admin_role_stmt))

        if admin_role:
            # Get list of permission-api.assoc_permission_api_id of the admin role
            stmt = (
                select(PermissionApi)
                .where(
                    and_(
                        ~PermissionApi.roles.contains(admin_role),
                        ~Api.name.in_(admin_ignored_apis),
                    )
                )
                .join(Api)
            )
            result = await safe_call(db.scalars(stmt))
            existing_assoc_permission_api_roles = result.all()

            # Add admin role to all permission-api objects
            for permission_api in existing_assoc_permission_api_roles:
                permission_api.roles.append(admin_role)
                logger.info(
                    f"ASSOCIATING {admin_role} WITH PERMISSION-API {permission_api}"
                )
            await safe_call(db.commit())

    def _mount_static_folder(self):
        """
        Mounts the static folder specified in the configuration.

        Returns:
            None
        """
        # If the folder does not exist, create it
        os.makedirs(g.config.get("STATIC_FOLDER", DEFAULT_STATIC_FOLDER), exist_ok=True)

        static_folder = g.config.get("STATIC_FOLDER", DEFAULT_STATIC_FOLDER)
        self.app.mount("/static", StaticFiles(directory=static_folder), name="static")

    def _mount_template_folder(self):
        """
        Mounts the template folder specified in the configuration.

        Returns:
            None
        """
        # If the folder does not exist, create it
        os.makedirs(
            g.config.get("TEMPLATE_FOLDER", DEFAULT_TEMPLATE_FOLDER), exist_ok=True
        )

        templates = Jinja2Templates(
            directory=g.config.get("TEMPLATE_FOLDER", DEFAULT_TEMPLATE_FOLDER)
        )

        @self.app.get("/{full_path:path}", response_class=HTMLResponse)
        def index(request: Request):
            try:
                return templates.TemplateResponse(
                    request=request,
                    name="index.html",
                    context={"base_path": g.config.get("BASE_PATH", "/")},
                )
            except TemplateNotFound:
                raise HTTPException(status_code=404, detail="Not Found")

    """
    -----------------------------------------
         INIT FUNCTIONS
    -----------------------------------------
    """

    def _init_config(self):
        """
        Initializes the configuration for the FastAPI application.

        This method reads the configuration values from the `g.config` dictionary and sets the corresponding attributes
        of the FastAPI application.
        """
        if self.app:
            self.app.title = g.config.get("APP_NAME", "FastAPI React Toolkit")
            self.app.summary = g.config.get("APP_SUMMARY", self.app.summary)
            self.app.description = g.config.get("APP_DESCRIPTION", self.app.description)
            self.app.version = g.config.get("APP_VERSION", __version__)
            self.app.openapi_url = g.config.get("APP_OPENAPI_URL", self.app.openapi_url)

    def _init_lifespan(self):
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Run when the app is starting up
            self.connect_to_database()

            if self.create_tables:
                await session_manager.create_all()

            # Creating permission, apis, roles, and connecting them
            await self.init_database()

            # On startup
            if self.on_startup:
                await safe_call(self.on_startup(app))

            yield

            # On shutdown
            if self.on_shutdown:
                await safe_call(self.on_shutdown(app))

            # Run when the app is shutting down
            await session_manager.close()

        # Check whether lifespan is already set
        if not isinstance(self.app.router.lifespan_context, _DefaultLifespan):
            raise ValueError(
                "Lifespan already set, please do not set lifespan directly in the FastAPI app"
            )

        self.app.router.lifespan_context = lifespan

    def _init_info_api(self):
        from .apis import InfoApi

        self.add_api(InfoApi)

    def _init_auth_api(self):
        from .apis import AuthApi

        self.add_api(AuthApi)

    def _init_users_api(self):
        from .apis import UsersApi

        self.add_api(UsersApi)

    def _init_roles_api(self):
        from .apis import RolesApi

        self.add_api(RolesApi)

    def _init_permissions_api(self):
        from .apis import PermissionsApi

        self.add_api(PermissionsApi)

    def _init_apis_api(self):
        from .apis import ViewsMenusApi

        self.add_api(ViewsMenusApi)

    def _init_permission_apis_api(self):
        from .apis import PermissionViewApi

        self.add_api(PermissionViewApi)

    def _init_basic_apis(self):
        self._init_info_api()
        self._init_auth_api()
        self._init_users_api()
        self._init_roles_api()
        self._init_permissions_api()
        self._init_apis_api()
        self._init_permission_apis_api()

    def _init_js_manifest(self):
        @self.app.get("/server-config.js", response_class=StreamingResponse)
        def js_manifest():
            env = Environment(autoescape=select_autoescape(["html", "xml"]))
            template_string = "window.fab_react_config = {{ react_vars |tojson }}"
            template = env.from_string(template_string)
            rendered_string = template.render(
                react_vars=json.dumps(g.config.get("FAB_REACT_CONFIG", {}))
            )
            content = rendered_string.encode("utf-8")
            scriptfile = io.BytesIO(content)
            return StreamingResponse(
                scriptfile,
                media_type="application/javascript",
            )

    """
    -----------------------------------------
         USER MANAGER FUNCTIONS
    -----------------------------------------
    """

    async def get_user(
        self,
        email_or_username: str,
        session: AsyncSession | Session | None = None,
    ):
        """
        Gets the user with the specified email or username.

        Args:
            email_or_username (str): The email or username of the user.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The user object.

        Raises:
            UserNotExists: If the user with the specified email or username does not exist.
        """
        if session:
            return await self._get_user(session, email_or_username)

        async with session_manager.session() as db:
            return await self._get_user(db, email_or_username)

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        roles: list[str] | None = None,
        session: AsyncSession | Session | None = None,
    ):
        """
        Creates a new user with the given information.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            first_name (str, optional): The first name of the user. Defaults to "".
            last_name (str, optional): The last name of the user. Defaults to "".
            roles (list[str] | None, optional): The roles assigned to the user. Defaults to None.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The created user object.

        Raises:
            SomeException: Description of the exception raised, if any.
        """

        if session:
            return await self._create_user(
                session,
                username,
                email,
                password,
                first_name,
                last_name,
                roles,
            )

        async with session_manager.session() as db:
            return await self._create_user(
                db, username, email, password, first_name, last_name, roles
            )

    async def create_role(
        self, name: str, session: AsyncSession | Session | None = None
    ):
        """
        Creates a new role with the given name.

        Args:
            name (str): The name of the role to create.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            Role: The created role object.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            return await self._create_role(session, name)

        async with session_manager.session() as db:
            return await self._create_role(db, name)

    async def reset_password(
        self,
        user: User,
        new_password: str,
        session: AsyncSession | Session | None = None,
    ):
        """
        Resets the password of the specified user.

        Args:
            user (User): The user whose password is to be reset.
            new_password (str): The new password to set.
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            User: The user object with the updated password.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            return await self._reset_password(session, user, new_password)

        async with session_manager.session() as db:
            return await self._reset_password(db, user, new_password)

    async def _get_user(self, session: AsyncSession | Session, email_or_username: str):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        try:
            return await manager.get_by_email(email_or_username)
        except UserNotExists:
            return await manager.get_by_username(email_or_username)

    async def export_data(
        self,
        data: Literal["users", "roles"],
        type: Literal["json", "csv"] = "json",
        session: AsyncSession | Session | None = None,
    ):
        """
        Exports the specified data to a file.

        Args:
            data (Literal["users", "roles"]): The data to export (users or roles).
            type (Literal["json", "csv"], optional): The type of file to export the data to. Defaults to "json".
            session (AsyncSession | Session | None, optional): The database session to use. Defaults to None.

        Returns:
            str: The exported data in JSON or CSV format.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        if session:
            match data:
                case "users":
                    return await self._export_users(session, type)
                case "roles":
                    return await self._export_roles(session, type)

        async with session_manager.session() as db:
            match data:
                case "users":
                    return await self._export_users(db, type)
                case "roles":
                    return await self._export_roles(db, type)

    async def _create_user(
        self,
        session: AsyncSession | Session,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        roles: list[str] | None = None,
    ):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        return await manager.create(
            UserCreate(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            ),
            roles,
        )

    async def _create_role(
        self,
        session: AsyncSession | Session,
        name: str,
    ):
        role = Role(name=name)
        session.add(role)
        await safe_call(session.commit())
        return role

    async def _reset_password(
        self, session: AsyncSession | Session, user: User, new_password: str
    ):
        manager = next(g.auth.get_user_manager(UserDatabase(session, User)))
        token = await manager.forgot_password(user)
        return await manager.reset_password(token, new_password)

    async def _export_users(
        self, session: AsyncSession | Session, type: Literal["json", "csv"] = "json"
    ):
        stmt = select(User)
        users = await safe_call(session.scalars(stmt))
        user_dict = {}
        for user in users:
            user_dict[user.username] = UserReadWithPassword.model_validate(
                user
            ).model_dump()
        if type == "json":
            return json.dumps(user_dict, indent=4)

        csv_data = "Username,Data\n"
        for username, data in user_dict.items():
            csv_data += f"{username},{data}\n"
        return csv_data

    async def _export_roles(
        self, session: AsyncSession | Session, type: Literal["json", "csv"] = "json"
    ):
        stmt = select(Role)
        roles = await safe_call(session.scalars(stmt))
        role_dict = {}
        for role in roles:
            # TODO: Change result
            role_dict[role.name] = RoleSchema.model_validate(role).model_dump()
        if type == "json":
            return json.dumps(role_dict, indent=4)

        csv_data = "Role,Data\n"
        for role, data in role_dict.items():
            csv_data += f"{role},{','.join(data)}\n"
        return csv_data

    """
    -----------------------------------------
         SECURITY FUNCTIONS
    -----------------------------------------
    """

    async def cleanup(self, session: AsyncSession | Session | None = None):
        """
        Cleanup unused permissions from apis and roles.

        Returns:
            None
        """
        if session:
            return await self._cleanup(session)

        async with session_manager.session() as db:
            return await self._cleanup(db)

    async def _cleanup(self, session: AsyncSession | Session):
        if g.is_migrate:
            self._init_basic_apis()

        api_permission_tuples = (
            g.config.get("ROLES") or g.config.get("FAB_ROLES", {})
        ).values()
        apis = [api.__class__.__name__ for api in self.apis]
        permissions = self.total_permissions()
        for api_permission_tuple in api_permission_tuples:
            for api, permission in api_permission_tuple:
                apis.append(api)
                permissions.append(permission)

        # Clean up unused permissions
        unused_permissions = await safe_call(
            session.scalars(select(Permission).where(~Permission.name.in_(permissions)))
        )
        for permission in unused_permissions:
            logger.info(f"DELETING PERMISSION {permission} AND ITS ASSOCIATIONS")
            await safe_call(session.delete(permission))

        # Clean up unused apis
        unused_apis = await safe_call(
            session.scalars(select(Api).where(~Api.name.in_(apis)))
        )
        for api in unused_apis:
            logger.info(f"DELETING API {api} AND ITS ASSOCIATIONS")
            await safe_call(session.delete(api))

        await safe_call(session.commit())

    """
    -----------------------------------------
         PROPERTY FUNCTIONS
    -----------------------------------------
    """

    @property
    def config(self):
        return g.config
