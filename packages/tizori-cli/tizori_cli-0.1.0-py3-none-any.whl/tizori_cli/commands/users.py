import string
from typer import Typer, Option
from rich import print
from typing_extensions import Annotated


from tizori_cli.wrapper import users, roles
from tizori_cli.commands.base import base_wrapper


users_app = Typer()

def clean_and_split_roles(roles_str):
    # Define characters to remove
    chars_to_remove = string.whitespace + '[](){}'

    # Create a translation table to map each character in chars_to_remove to None
    translation_table = str.maketrans('', '', chars_to_remove)

    # Remove specified characters from the roles string
    cleaned_roles_str = roles_str.translate(translation_table)

    # Split the cleaned string by commas to get a list of roles
    roles_list = cleaned_roles_str.split(',')

    # Return the list of roles
    return roles_list

@users_app.command("list")
def list_users():
    status, users_list = users.list_users(base_wrapper)
    if status:
        print("\n[bold blue]Users[/bold blue]")
        for user in users_list:
            print(f"\nUsername: [bold]{user.get('username')}[/bold]")
            print(f"Email: [bold]{user.get('email')}[/bold]")
            print(f"Name: [bold]{user.get('name')}[/bold]")
    else:
        print(f"\n[red]Error[/red]: {users_list}")

@users_app.command("get")
def get_user(
    username: Annotated[str, Option(help="Username", prompt=True)],
):
    status, user = users.get_user(base_wrapper, username)
    if status:
        print("\n[bold blue]User[/bold blue]")
        print(f"Username: [green]{user.get('username')}[/green]")
        print(f"Email: [green]{user.get('email')}[/green]")
        print(f"Name: [green]{user.get('name')}[/green]")
        print("Roles:")
        for role in user.get("roles"):
            print(f"[green]{role.get("name")} - {role.get("id")}[/green]")
    else:
        print(f"\n[red]Error[/red]: {user}")

@users_app.command("create")
def create_user(
    username: Annotated[str, Option(help="Username", prompt=True)],
    email: Annotated[str, Option(help="Email", prompt=True)],
    name: Annotated[str, Option(help="Name", prompt=True)],
):
    status, message = users.create_user(base_wrapper, username, email, name)
    if status:
        print("\n[green]User Created![/green]")
        # Display generated password
        print(f"Password: [bold blue]{message}[/bold blue]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@users_app.command("update")
def update_user(
    username: Annotated[str, Option(help="Username", prompt=True)],
    email: Annotated[str, Option(help="Email", prompt=True)],
    name: Annotated[str, Option(help="Name", prompt=True)],
):
    data = {"email": email, "name": name}
    status, message = users.update_user(base_wrapper, username, data)
    if status:
        print("\n[green]User Updated![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@users_app.command("update-roles")
def update_user_roles(
    username: Annotated[str, Option(help="Username", prompt=True)],
    roles: Annotated[str, Option(help="Roles", prompt=True)],
):
    roles = clean_and_split_roles(roles)
    # status, roles_list = roles.list_roles(base_wrapper)
    # if not status:
    #     print(f"\n[red]Error[/red]: {roles_list}")
    #     return
    # roles_dict = {role.get("name"): role.get("id") for role in roles_list}
    data = {"roles": roles}
    status, message = users.update_user(base_wrapper, username, data)
    if status:
        print("\n[green]User Roles Updated![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@users_app.command("delete")
def delete_user(
    username: Annotated[str, Option(help="Username", prompt=True)],
):
    status, message = users.delete_user(base_wrapper, username)
    if status:
        print("\n[green]User Deleted![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")
    