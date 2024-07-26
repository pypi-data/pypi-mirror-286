import typer

from picfix.commands.convert import convert_app
from picfix.commands.optimize import optimize_app
from picfix.commands.resize import resize_app

app = typer.Typer(name="picfix", no_args_is_help=True)

app.add_typer(
    resize_app,
    name="resize",
    help="resize images to specified dimnsions",
    no_args_is_help=True,
)
app.add_typer(
    convert_app, name="convert", help="convert image formats", no_args_is_help=True
)
app.add_typer(
    optimize_app,
    name="optimize",
    help="optimize images to reduce file size",
    no_args_is_help=True,
)

if __name__ == "__main__":
    app()
