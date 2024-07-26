from typing import Optional
from typing_extensions import Annotated
import typer
from .db_populate import NvdDatabase
from . import __app_name__, __version__
import os

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def init():
    """
    Initialize the users database.
    """
    if os.environ.get('NVD_API_KEY'):
        api_key = os.environ.get('NVD_API_KEY')
        NVD = NvdDatabase(api_key)
        total_cves = NVD.dump_nvd()
        
        if total_cves:
            typer.secho(f"NVD initialized successfully with {total_cves} cves", fg=typer.colors.GREEN)
        else:
            typer.secho("Error initializing the database", fg=typer.colors.RED)
   
    else:
        typer.echo("Please export NVD_API_KEY")
        raise typer.Exit()
       
        