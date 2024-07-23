import os
import yaml
from typing import Iterator

from synthetic_open_schema_model import v1beta1


def resource_loader(resource_dict: dict) -> object:
    """
    Load and instantiate a class based on the provided resource dictionary.

    Args:
        resource_dict (dict): Dictionary containing resource data.

    Returns:
        object: Instance of the class specified by the 'kind' field in resource_dict.

    Raises:
        AssertionError: If 'apiVersion' is not 'checks.dev/v1beta1'.
        AssertionError: If 'kind' field is missing or invalid.
    """

    api_version = resource_dict.get("apiVersion")
    assert api_version == "checks.dev/v1beta1", "Invalid apiVersion"

    kind = resource_dict.get("kind")
    assert kind, "kind is required"

    kind_class = getattr(v1beta1, kind, None)
    assert kind_class, f"Invalid kind: {kind} for apiVersion: {api_version}"

    return kind_class(**resource_dict)


def load_files(files: list[str]) -> Iterator[object]:
    """
    Load resources from YAML files specified in the list of file paths.

    Args:
        files (list[str]): List of file paths to YAML files containing resource definitions.

    Yields:
        object: Each resource loaded from the YAML files as instantiated objects.

    Raises:
        ValueError: If there are duplicate resource names found across the loaded files.
    """
    resources = set()
    for file in files:
        with open(file) as fp:
            for resource in yaml.safe_load_all(fp):
                if resource["metadata"]["name"] in resources:
                    raise ValueError(
                        f"Duplicate resource name: {resource['metadata']['name']}"
                    )

                resources.add(resource["metadata"]["name"])
                yield resource_loader(resource)


def load_dir_recursively(directory: str) -> Iterator[str]:
    """
    Recursively yield relative paths of all files in a directory.

    Args:
        directory (str): Directory path to recursively search for files.

    Yields:
        str: Relative path of each file found within the directory and its subdirectories.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.relpath(os.path.join(root, file), directory)


def load_directory(directory: str) -> Iterator[object]:
    """
    Load resources from YAML files within a directory and its subdirectories.

    Args:
        directory (str): Directory path containing YAML resource files.

    Returns:
        Iterator[object]: Iterator yielding each resource loaded from the YAML files as instantiated objects.

    Example:
        Consider a directory structure like this:
        ```
        /resources
        ├── file1.yaml
        ├── subdir
        │   └── file2.yaml
        └── file3.yaml
        ```
        Calling `load_directory('/resources')` will yield each resource object loaded from `file1.yaml`,
        `subdir/file2.yaml`, and `file3.yaml`. It ensures no duplicate resource names exist across
        the loaded resources.

    """
    return load_files(
        map(
            lambda file: os.path.join(directory, file),
            sorted(load_dir_recursively(directory)),
        )
    )
