from typer import Typer, Abort, Context, echo
from rich import print

from tizori_cli.config import load_config, save_config
from tizori_cli.commands.auth import auth_app
from tizori_cli.commands.users import users_app
from tizori_cli.commands.roles import roles_app
from tizori_cli.commands.applications import applications_app


app = Typer(context_settings={"help_option_names": ["-h", "--help"]})
app.add_typer(auth_app, name="auth")
app.add_typer(users_app, name="users")
app.add_typer(roles_app, name="roles")
app.add_typer(applications_app, name="apps")


@app.callback(invoke_without_command=True)
def callback(ctx: Context):
    config = load_config()

    # Show help if no subcommand is provided
    if ctx.invoked_subcommand is None:
        print(
            """
     [white]███████████████╗[/white]                 
    [white]███╔══════════███╗               
   [white]███╔╝           ███╗      ████████╗██╗███████╗ ██████╗ ██████╗ ██╗[/white]           
   [white]███║            ███║      ╚══██╔══╝██║╚══███╔╝██╔═══██╗██╔══██╗██║[/white]         
   [white]███║            ███║         ██║   ██║  ███╔╝ ██║   ██║██████╔╝██║[/white]         
[white]█████████████████████████╗      ██║   ██║ ███╔╝  ██║   ██║██╔══██╗██║[/white]        
[white]█████████████████████████║      ██║   ██║███████╗╚██████╔╝██║  ██║██║[/white]      
[white]██████████╔═════█████████║      ╚═╝   ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝[/white]    
[white]██████████║     █████████║[/white]       
[white]████████████╗ ███████████║[/white]      [bright_white]Developer:[/bright_white] [green]Dhruv Shah[/green]     
[white]████████████║ ███████████║[/white]      [bright_white]Github:[/bright_white] [blue]https://github.com/Dhruv9449[/blue]      
[white]████████████║ ███████████║[/white]      [bright_white]Repository:[/bright_white] [blue]https://github.com/Dhruv9449/tizori-cli[/blue]         
[white]█████████████████████████║[/white]         
[white]█████████████████████████║[/white]             
[white]╚════════════════════════╝[/white]       
"""
        )
        echo(ctx.get_help())

    # Check if the base URL is setit and command is not set-base-url
    if (config.get("base_url") == "" or config.get("base_url") is None) and ctx.invoked_subcommand != "set-base-url":
        print("\n[red]Base URL not set![/red]")
        print("Please set the base URL using the command: [bold blue]tizori set-base-url <URL>[/bold blue]")
        raise Abort()


@app.command("set-base-url")
def set_base_url(url: str):
    """
    Set the base URL for the API
    """
    config = load_config()
    config["base_url"] = url
    save_config(config)
    print(f"\nBase URL set to: [bold blue]{url}[/bold blue]")
