from typer import Typer, Option
from rich import print
from typing_extensions import Annotated


from tizori_cli.wrapper import roles
from tizori_cli.commands.base import base_wrapper

roles_app = Typer()

@roles_app.command("list")
def list_roles():
    status, roles_list = roles.list_roles(base_wrapper)
    if status:
        print("\n[bold blue]Roles[/bold blue]")
        for role in roles_list:
            print(f"\nName: [green]{role.get('name')}[/green]")
            print(f"ID: [green]{role.get('id')}[/green]")
    else:
        print(f"\n[red]Error[/red]: {roles_list}")

@roles_app.command("get")
def get_role(
    role_id: Annotated[str, Option(help="Role ID", prompt=True)],
):
    status, role = roles.get_role(base_wrapper, role_id)
    if status:
        print("\n[bold blue]Role[/bold blue]")
        print(f"Name: [green]{role.get('name')}[/green]")
        print(f"ID: [green]{role.get('id')}[/green]")
        print("Permissions:")
        for permission in role.get("permissions"):
            print(f"[green]{permission.get('scope')} - {permission.get('permission')}[/green]")
    else:
        print(f"\n[red]Error[/red]: {role}")

@roles_app.command("create")
def create_role(
    name: Annotated[str, Option(help="Name", prompt=True)],
):
    status, message = roles.create_role(base_wrapper, name)
    if status:
        print("\n[green]Role Created![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@roles_app.command("update")
def update_role(
    role_id: Annotated[str, Option(help="Role ID", prompt=True)],
    name: Annotated[str, Option(help="Name", prompt=True)],
):
    data = {"name": name}
    status, message = roles.update_role(base_wrapper, role_id, data)
    if status:
        print("\n[green]Role Updated![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@roles_app.command("add-permission")
def add_permissions_to_role(
    role_id: Annotated[str, Option(help="Role ID", prompt=True)],
    scope: Annotated[str, Option(help="Scope", prompt=True)],
    permission: Annotated[str, Option(help="Permission", prompt=True)],
):
    perm = {"scope": scope, "permission": permission}
    status, role = roles.get_role(base_wrapper, role_id)
    if not status:
        print(f"\n[red]Error[/red]: {role}")
        return
    permissions = role.get("permissions")
    if permissions is None:
        permissions = []
    data = {"permissions": permissions + [perm], "name": role.get("name")}
    status, message = roles.update_role(base_wrapper, role_id, data)
    if status:
        print("\n[green]Role Updated![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@roles_app.command("remove-permission")
def remove_permissions_from_role(
    role_id: Annotated[str, Option(help="Role ID", prompt=True)],
    scope: Annotated[str, Option(help="Scope", prompt=True)],
    permission: Annotated[str, Option(help="Permission", prompt=True)],
):
    perm = {"scope": scope, "permission": permission}
    status, role = roles.get_role(base_wrapper, role_id)
    if not status:
        print(f"\n[red]Error[/red]: {role}")
        return
    data = {"permissions": [p for p in role.get("permissions") if p != perm], "name": role.get("name")}
    status, message = roles.update_role(base_wrapper, role_id, data)
    if status:
        print("\n[green]Role Updated![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

@roles_app.command("delete")
def delete_role(
    role_id: Annotated[str, Option(help="Role ID", prompt=True)],
):
    status, message = roles.delete_role(base_wrapper, role_id)
    if status:
        print("\n[green]Role Deleted![/green]")
    else:
        print(f"\n[red]Error[/red]: {message}")

