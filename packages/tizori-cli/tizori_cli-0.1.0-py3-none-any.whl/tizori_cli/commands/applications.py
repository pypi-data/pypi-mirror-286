from typer import Typer, Option
from rich import print
from typing_extensions import Annotated


from tizori_cli.wrapper import applications
from tizori_cli.commands.base import base_wrapper


applications_app = Typer()

@applications_app.command("list")
def list_applications():
    status, applications_list = applications.list_applications(base_wrapper)
    if status:
        print("\n[bold blue]Applications[/bold blue]")
        for application in applications_list:
            print(f"\nName: [green]{application.get('name')}[/green]")
            print(f"ID: [green]{application.get('id')}[/green]")
    else:
        print(f"\n[red]Error[/red]: {applications_list}")

@applications_app.command("get-credentials")
def get_application_credentials(
    application_id: Annotated[str, Option(help="Application ID", prompt=True)],
):
    status, credentials = applications.get_application_credentials(base_wrapper, application_id)
    if status:
        print("\n[bold blue]Credentials[/bold blue]")
        print(f"Application: [green]{credentials.get('name')}[/green]")
        print(f"Username: [green]{credentials.get('credentials').get('username')}[/green]")
        print(f"Password: [green]{credentials.get('credentials').get('password')}[/green]")
    else:
        print(f"\n[red]Error[/red]: {credentials}")


@applications_app.command("create")
def create_application(
    name: Annotated[str, Option(help="Name", prompt=True)],
):
    status, message = applications.create_application(base_wrapper, name)
    if status:
        print("\n[bold green]Application created successfully[/bold green]")
    else:
        print(f"\n[red]Error[/red]: {message}")


@applications_app.command("update-credentials")
def update_application_credentials(
    application_id: Annotated[str, Option(help="Application ID", prompt=True)],
    username: Annotated[str, Option(help="Client ID", prompt=True)],
    password: Annotated[str, Option(help="Client Secret", prompt=True)],
):
    data = {"username": username, "password": password}
    status, message = applications.update_application_credentials(base_wrapper, application_id, data)
    if status:
        print("\n[bold green]Credentials updated successfully![/bold green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@applications_app.command("delete")
def delete_application(
    application_id: Annotated[str, Option(help="Application ID", prompt=True)],
):
    status, message = applications.delete_application(base_wrapper, application_id)
    if status:
        print("\n[bold green]Application deleted successfully![/bold green]")
    else:
        print(f"\n[red]Error[/red]: {message}")



