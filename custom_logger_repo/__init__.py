from importlib import import_module
from importlib import resources
import re

_already_imported = {}


def resolve_logger(version: str) -> None:
    """
    - Verify if required version package is in a repo 
    - Check if package is i a cache
    - Import package and save reference in a cache

    Args:
        version (str): required version 
        format example: "1.2.3" or "1_2_3" or reserved value "latest"
                but repo file MUST have verison format "1_2_3"
                    version can be on any position in a package name

    Raises:
        NameError: package file of required version not found in a folder

    Returns:
        Reference to loaded module
    """
    module = None
    # module file name in a repository, None if does not exists
    filename = file_max_version() if version == "latest" else file_version(version)
    try:
        # check cache if module already loaded
        module = _already_imported[filename]
    except KeyError as e:
        # attempt to load and cache module
        for package_filename in resources.contents(__name__):
            if package_filename == filename:
                module = import_module(f"{__name__}.{filename[:-3]}")
        if not module:
            raise NameError(f"Module in version {version} not found in package {__name__}") from e

        _already_imported[filename] = module
    return module


def file_version(version: str) -> str:
    """CHeck, if module name with required version exists in a folder

    Args:
        version : checked version

    Returns:
        str: package filename, None if does not exists
    """
    for filename in resources.contents(__name__):
        if re.search(version, filename):
            return filename


def file_max_version() -> str:
    """In a package looks for file with max version

    Returns:
        str: file name with max version; None if does not exists
    """

    max_version: int = -1
    max_version_file: str = None
    # All files in a folder with version in a name
    for filename in resources.contents(__name__):
        max_version_list = re.findall(r'[0-9]+', filename)

        if max_version_list:
            # List of string numbers to string equivalent
            a_string = "".join(max_version_list)
            # file version
            a_int = int(a_string)
            # max file version
            if a_int > max_version:
                max_version_file = filename
                max_version = a_int
    return max_version_file
