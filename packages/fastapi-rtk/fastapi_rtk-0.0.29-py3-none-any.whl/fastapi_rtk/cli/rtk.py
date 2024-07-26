import asyncio
from pathlib import Path
from typing import Annotated, Union

import typer

from ..globals import g
from .commands import cleanup as _cleanup
from .commands import create_user as _create_user
from .commands import export_data, path_callback
from .commands import reset_password as _reset_password
from .commands import version_callback
from .decorators import ensure_fastapi_rtk_tables_exist

rtk_app = typer.Typer(rich_markup_mode="rich")


@rtk_app.callback()
@ensure_fastapi_rtk_tables_exist
def callback(
    version: Annotated[
        Union[bool, None],
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
    path: Annotated[
        Union[Path, None],
        typer.Option(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]FastAPI[/bold] app. If not provided, a default set of paths will be tried.",
            callback=path_callback,
        ),
    ] = None,
) -> None:
    """
    FastAPI RTK CLI - The [bold]fastapi rtk[/bold] command line app. 😎

    Manage your [bold]FastAPI[/bold] users easily with this CLI.
    """


@rtk_app.command()
def create_admin(
    username: Annotated[
        str, typer.Option(..., help="The username of the admin user.")
    ] = "",
    email: Annotated[str, typer.Option(..., help="The email of the admin user.")] = "",
    password: Annotated[
        str, typer.Option(..., help="The password of the admin user.")
    ] = "",
    first_name: Annotated[
        str, typer.Option(..., help="The first name of the admin user.")
    ] = "",
    last_name: Annotated[
        str, typer.Option(..., help="The last name of the admin user.")
    ] = "",
):
    """
    Create an admin user. This user will have the admin role. If the role does not exist, it will be created.
    """
    while not username:
        username = typer.prompt("Username (required)")
        if not username:
            typer.echo("Username is required.")
    while not email:
        email = typer.prompt("Email (required)")
        if not email:
            typer.echo("Email is required.")
    while not password:
        new_password = typer.prompt("Password", hide_input=True)
        confirm_password = typer.prompt("Confirm Password", hide_input=True)
        if new_password != confirm_password:
            typer.echo("Passwords do not match. Please try again.")
            continue
        password = new_password
    if not first_name:
        first_name = typer.prompt("First Name (Optional)")
    if not last_name:
        last_name = typer.prompt("Last Name (Optional)")

    user = asyncio.run(
        _create_user(
            username, email, password, first_name, last_name, g.admin_role, True
        )
    )

    typer.echo(f"Admin user {user.username} created successfully.")


@rtk_app.command()
def create_user(
    username: Annotated[str, typer.Option(..., help="The username of the user.")] = "",
    email: Annotated[str, typer.Option(..., help="The email of the user.")] = "",
    password: Annotated[str, typer.Option(..., help="The password of the user.")] = "",
    first_name: Annotated[
        str, typer.Option(..., help="The first name of the user.")
    ] = "",
    last_name: Annotated[
        str, typer.Option(..., help="The last name of the user.")
    ] = "",
    role: Annotated[
        str,
        typer.Option(
            ...,
            help="The role of the user. Defaults to AUTH_PUBLIC_ROLE in config or 'public' if create_role is True.",
        ),
    ] = "",
    create_role: Annotated[
        bool,
        typer.Option(
            ...,
            help="Create the role if it does not exist. Defaults to False.",
        ),
    ] = False,
):
    """
    Create a user. If create_role is True, the role will be created if it does not exist.
    """
    while not username:
        username = typer.prompt("Username (required)")
        if not username:
            typer.echo("Username is required.")
    while not email:
        email = typer.prompt("Email (required)")
        if not email:
            typer.echo("Email is required.")
    while not password:
        new_password = typer.prompt("Password", hide_input=True)
        confirm_password = typer.prompt("Confirm Password", hide_input=True)
        if new_password != confirm_password:
            typer.echo("Passwords do not match. Please try again.")
            continue
        password = new_password
    if not first_name:
        first_name = typer.prompt("First Name (Optional)")
    if not last_name:
        last_name = typer.prompt("Last Name (Optional)")

    if create_role and not role:
        role = g.public_role
    user = asyncio.run(
        _create_user(
            username, email, password, first_name, last_name, role, create_role
        )
    )

    typer.echo(f"User {user.username} with role {role} created successfully.")


@rtk_app.command()
def reset_password(
    email_or_username: Annotated[
        str, typer.Option(..., help="The email or username of the user.")
    ] = "",
    password: Annotated[str, typer.Option(..., help="The new password.")] = "",
):
    """
    Reset the password of a user.
    """
    while not email_or_username:
        email_or_username = typer.prompt("Email or Username (required)")
        if not email_or_username:
            typer.echo("Email or Username is required.")
    while not password:
        new_password = typer.prompt("Password", hide_input=True)
        confirm_password = typer.prompt("Confirm Password", hide_input=True)
        if new_password != confirm_password:
            typer.echo("Passwords do not match. Please try again.")
            continue
        password = new_password

    user = asyncio.run(_reset_password(email_or_username, password))

    typer.echo(f"Password reset for user {user.username}.")


@rtk_app.command()
def export_users(
    file_path: Annotated[
        str, typer.Option(..., help="The path to the file to export the users to.")
    ] = "",
    type: Annotated[
        str,
        typer.Option(
            ...,
            help="The type of file to export the users to. Defaults to json.",
        ),
    ] = "json",
):
    """
    Export users to a file.
    """
    while not file_path:
        file_path = typer.prompt("File Path (required)")
        if not file_path:
            typer.echo("File Path is required.")

    asyncio.run(export_data(file_path, "users", type))

    typer.echo(f"Users exported to {file_path}.")


@rtk_app.command()
def export_roles(
    file_path: Annotated[
        str, typer.Option(..., help="The path to the file to export the roles to.")
    ] = "",
    type: Annotated[
        str,
        typer.Option(
            ...,
            help="The type of file to export the roles to. Defaults to json.",
        ),
    ] = "json",
):
    """
    Export roles to a file.
    """
    while not file_path:
        file_path = typer.prompt("File Path (required)")
        if not file_path:
            typer.echo("File Path is required.")

    asyncio.run(export_data(file_path, "roles", type))

    typer.echo(f"Roles exported to {file_path}.")


@rtk_app.command()
def cleanup():
    """
    Cleanup unused permissions from apis and roles.
    """
    asyncio.run(_cleanup())

    typer.echo("Cleanup complete.")
