import os
import uuid
import yaml
from typing import Dict, Optional


# Path to the configuration file
conf_file: str = os.path.expanduser("~/.checks.dev.yaml")


def update_conf(conf: Dict[str, str]) -> None:
    """
    Update the YAML configuration file with the provided dictionary.

    Args:
        conf (Dict[str, str]): Dictionary containing configuration data.

    Returns:
        None
    """
    with open(conf_file, "w") as f:
        f.write(yaml.safe_dump(conf))


def load_or_create_conf() -> Dict[str, str]:
    """
    Load the YAML configuration file if it exists, otherwise create a new one with a default client_id.

    Returns:
        Dict[str, str]: Configuration dictionary.
    """
    if not os.path.exists(conf_file):
        conf: Dict[str, str] = {"client_id": uuid.uuid4().hex}
        update_conf(conf)
        return conf
    else:
        with open(conf_file) as f:
            return yaml.safe_load(f)


def get_client_id() -> str:
    """
    Retrieve the client_id from the configuration file. If not present, generate a new one and update the file.

    Returns:
        str: Client ID.
    """
    conf: Dict[str, str] = load_or_create_conf()
    if "client_id" not in conf:
        conf["client_id"] = uuid.uuid4().hex
        update_conf(conf)

    return conf["client_id"]


def get_token() -> Optional[str]:
    """
    Retrieve the token from the configuration file.

    Returns:
        Optional[str]: Token if present, otherwise None.
    """
    conf: Dict[str, str] = load_or_create_conf()
    return conf.get("token")


def load_host() -> Optional[str]:
    """
    Retrieve the account's host from the configuration file.

    Returns:
        Optional[str]: host if present, otherwise None.
    """
    conf: Dict[str, str] = load_or_create_conf()
    return conf.get("host")


def save_token(token: str, account_host: str) -> None:
    """
    Save the token to the configuration file.

    Args:
        token (str): Token to save.

    Returns:
        None
    """
    conf: Dict[str, str] = load_or_create_conf()
    conf["token"] = token
    conf["host"] = account_host
    update_conf(conf)