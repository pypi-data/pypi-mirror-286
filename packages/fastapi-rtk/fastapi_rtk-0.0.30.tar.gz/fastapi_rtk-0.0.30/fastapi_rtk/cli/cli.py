from fastapi_cli.cli import app

from .db import db_app
from .rtk import rtk_app

app.add_typer(db_app, name="db")
app.add_typer(rtk_app, name="rtk")
