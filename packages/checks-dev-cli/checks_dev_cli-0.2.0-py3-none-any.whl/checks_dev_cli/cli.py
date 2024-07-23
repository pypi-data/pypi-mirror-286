import datetime
import json
import os
import sys
import time
from typing import Optional
import uuid
from pydantic import ValidationError
import requests
import typer
import yaml

from checks_dev_cli.conf import get_client_id, get_token, load_host, save_token
from checks_dev_cli.file_utils import load_directory, load_files

CHECKS_HOST = os.environ.get("CHECKS_HOST", "https://checks.dev")
cli = typer.Typer()


def load_token():
    """
    Load token from environment variable or config file.
    """
    return os.environ.get("CHECKS_TOKEN") or get_token()


def load(files, directory):
    assert not all(
        [files, directory]
    ), "Either file or directory must be provided, not both."
    assert any([files, directory]), "Either file or directory must be provided."

    resources = load_files(files) if files else load_directory(directory)
    return resources


@cli.command()
def sync(
    # project: Optional[str],
    file: Optional[list[str]] = typer.Option(None, help="File(s) to sync"),
    directory: Optional[str] = typer.Option(None, help="Directory to sync"),
    trim: Optional[bool] = typer.Option(False, help="Delete existing resources no longer present in the file or directory"),
    dry_run: Optional[bool] = typer.Option(False, help="Dry run mode")
):
    """Sync checks to check.dev service"""
    token = load_token()
    host = load_host() or CHECKS_HOST
    if not token:
        typer.echo("No token was found, authenticate using `checks auth`")
        sys.exit(1)

    resources = list(load(file, directory))

    typer.echo(f"Syncing {len(resources)} checks.")
    
    token = load_token()
    if not token:
        typer.echo("No token was found, authenticate using `checks auth`")
        sys.exit(1)

    res = requests.put(
        f"{host}/api/checks/sync",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "resources": [
                r.model_dump() for r in resources
            ],
            "trim": trim,
            "dry_run": dry_run
        }
    )

    jr = res.json()
    errors = jr.get("errors", [])
    if errors:
        typer.echo(f"Failed to sync due to {len(errors)} errors.")
        for error in errors:
            typer.echo(f"Error: {error}")
        sys.exit(1)

    else:
        typer.echo("Synced successfully.")
        for created in jr.get("created", []):
            typer.echo(f" Created: {created}")

        for updated in jr.get("updated", []):
            typer.echo(f" Updated: {updated}")

        for deleted in jr.get("deleted", []):
            typer.echo(f" Deleted: {deleted}")

        for orphaned in jr.get("orphaned", []):
            typer.echo(f" Orphaned: {orphaned}")


@cli.command()
def validate(
    file: Optional[list[str]] = typer.Option(None, help="File(s) to sync"),
    directory: Optional[str] = typer.Option(None, help="Directory to sync"),
):
    """Load checks from yaml files and validate"""

    resources = load(file, directory)

    idx = 0
    for resource in resources:
        idx += 1
        typer.echo(f"{idx} {resource.kind}: {resource.metadata.name}")

    typer.echo(f"Found {idx} resources.")



@cli.command()
def me():
    """Show current user"""
    token = load_token()
    if not token:
        typer.echo("No token was found, authenticate using `checks auth`")
        sys.exit(1)

    res = requests.get(f"{CHECKS_HOST}/api/auth/me/", headers={"Authorization": f"Bearer {token}"})
    jr = res.json()
    typer.echo(f"User: {jr['name']} <{jr['email']}>")

@cli.command()
def auth(account: str = typer.Option(..., help="Account name")):
    """Authenticate and save token"""

    session_id = uuid.uuid4().hex
    device_id = get_client_id()
    rqs = requests.Session()

    rqs.headers.update({
        "X-Session-Id": session_id,
        "X-Device-Id": device_id,
        "X-Account": account,
    })

    typer.echo(f"Session ID: {session_id}")
    typer.echo(f"Device ID: {device_id}")

    res = rqs.post(f"{CHECKS_HOST}/api/auth/authorize-client")
    jr = res.json()
    signature = jr["signature"]
    account_host = jr["account_host"]

    approval_link = f"{account_host}/auth/authorize?session_id={session_id}&signature={signature}"
    typer.echo(f"Please visit the link above to authenticate: {approval_link}")
    
    rqs.headers.update({
        "X-Signature": signature
    })

    when_started = datetime.datetime.now()
    while True:
        res = rqs.get(f"{CHECKS_HOST}/api/auth/client-token")
        if res.status_code == 200:
            token = res.json()["token"]
            save_token(token, account_host)
            typer.echo("Authenticated successfully, token saved.")
            break

        if datetime.datetime.now() - when_started > datetime.timedelta(minutes=5):
            typer.echo("Authentication timed out.")
            break
        time.sleep(3)


