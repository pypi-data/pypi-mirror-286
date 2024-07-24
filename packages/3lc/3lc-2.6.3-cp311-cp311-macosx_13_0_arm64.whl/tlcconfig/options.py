# =============================================================================
# <copyright>
# Copyright (c) 2023 3LC Inc. All rights reserved.
#
# All rights are reserved. Reproduction or transmission in whole or in part, in
# any form or by any means, electronic, mechanical or otherwise, is prohibited
# without the prior written permission of the copyright owner.
# </copyright>
# =============================================================================


"""
Configuration options for 3LC

This module contains the configuration options for 3LC. These options can be set in a config file, as environment
variables, or as command line arguments when launching the object service.

"""

from __future__ import annotations

import importlib.metadata
import logging
import os
from functools import partial
from typing import Any, Callable, Dict, List, Union

import platformdirs

# CONSTANTS ###################################################################

_logger = logging.getLogger("tlcconfig")


def get_default_root_dir() -> str:
    """Return the default root directory. This directory has a "projects" subdir that contains 3LC projects.

    This function is platform dependent, and the default is platform dependent:

    - Linux: `$HOME/.local/share/3LC/` or `$XDG_DATA_HOME/3LC/`
    - macOS: `$HOME/Library/Application Support/3LC/`
    - Windows: `%LOCALAPPDATA%\\3LC\\3LC\\`

    :returns: The default root directory.
    """

    return platformdirs.user_data_dir(appname="3LC", appauthor="3LC")


def get_default_log_dir() -> str:
    """Return the default log root directory.

    This function is platform dependent, and the default is platform dependent:

    - Linux: `$HOME/.local/state/3LC/log` or `$XDG_STATE_HOME/3LC/log`
    - macOS: `$HOME/Library/Logs/3LC/Logs`
    - Windows: `%LOCALAPPDATA%\\3LC\\3LC\\Logs`

    :returns: The default log root directory.
    """

    return platformdirs.user_log_dir(appname="3LC", appauthor="3LC")


def get_default_config_dir() -> str:
    """Return the default config file directory.

    This function is platform dependent, and the default is platform dependent:

    - Linux: `$HOME/.config/3LC` or `$XDG_CONFIG_HOME/3LC`
    - macOS: `$HOME/Library/Application Support/3LC`
    - Windows: `%LOCALAPPDATA%\\3LC\\3LC`

    :returns: The default config file directory.
    """

    return platformdirs.user_config_dir(appname="3LC", appauthor="3LC")


def _get_default_api_key_file_path() -> str:
    """Return the default API key file path in the config directory.

    :returns: The default API key file path.
    """

    API_KEY_FILE_NAME = "api_key.txt"
    return f"{get_default_config_dir()}{os.path.sep}{API_KEY_FILE_NAME}"


def _get_effective_api_key_file_path() -> str:
    """Return the effective API key file, which will be the default unless overridden by setting TLC_API_KEY_FILE.

    :returns: The effective API key file path.
    """

    return os.environ.get("TLC_API_KEY_FILE", _get_default_api_key_file_path())


def _get_default_telemetry() -> int:
    """Get the default telemetry value.

    If the tlc-enterprise package is installed, telemetry will be disabled by default.

    :returns: The default telemetry value.
    """
    try:
        importlib.metadata.distribution("tlc_enterprise")
        return 0
    except ImportError:
        return 1


def _consider_expandvars(path: str) -> str:
    """Expand a path if it does not begin with a schema definition.

    This function is platform dependent.
    E.g. "~/3LC" will be expanded to "/home/user/3LC" on Linux. But s3://~/3LC will not be expanded.
    """
    if not isinstance(path, str):
        raise ValueError(f"Expected string, got {type(path)}")

    if path.find("://") != -1:
        return path
    elif path.startswith("$."):
        # special expansion syntax, catches $. and $.. and ..., will be replaced later in the pipeline
        # find the first non . an run normpath on the rest
        i = 2
        while i < len(path) and path[i] == ".":
            i += 1
        expanded_path = path[:i] + os.path.expandvars(path[i:])
        return expanded_path
    else:
        expanded_path = os.path.normpath(os.path.expandvars(os.path.expanduser(path)))
        return expanded_path


def _ensure_dir_is_writeable(path: str) -> bool:
    """Ensure that a directory is writeable.

    If the directory starts with a schema (e.g. s3://, https://, etc.), this function will return True.

    If the directory does not exists, it will be created. If it exists, it will be checked for write access.

    :return: True if the directory is writeable, False otherwise.
    """

    if str(path).find("://") != -1:
        return True

    expanded_path = _consider_expandvars(path)

    if not os.path.exists(expanded_path):
        _logger.debug(f"Creating directory {expanded_path}")
        os.makedirs(expanded_path)

    return os.access(expanded_path, os.W_OK)


def _ensure_file_is_writeable(path: str) -> bool:
    """Ensure that a directory for a file is writeable.

    If the directory starts with a schema (e.g. s3://, https://, etc.), this function will return True.

    If the directory does not exists, it will be created. If it exists, it will be checked for write access.

    :return: True if the directory is writeable, False otherwise.
    """

    return _ensure_dir_is_writeable(os.path.dirname(path))


def _any_to_bool(input: Any) -> bool:
    if not isinstance(input, str):
        return bool(input)

    # Define strings that should explicitly return False
    false_strings = ["false", "no", "0", "none", "null", ""]

    # Convert the input string to lower case to make the function case-insensitive
    input_string_lower = input.strip().lower()

    # Check if the input string is in the list of false strings
    if input_string_lower in false_strings:
        return False
    # If not, return True (assuming any string not explicitly false is true)
    else:
        return True


def _dictify(value: Any, key: str, inner: Callable | None = None) -> dict[str, Any]:
    """Convert a value to a dictionary with a single key-value pair.

    :param value: The value to convert.
    :param key: The key to use in the dictionary.
    :param inner: A function to apply to the value before adding it to the dictionary.
    :returns: The dictionary with the key-value pair.
    """

    if isinstance(value, dict):
        if key not in value:
            raise ValueError(f"Expected key {key} in dictionary {value}")
        return {**value, key: inner(value[key]) if inner else value[key]}

    return {key: inner(value) if inner else value}


class OPTION:
    """Base class for all 3LC options"""

    default: Any = None
    """The default value for this option if it is not specified anywhere."""

    envvar: str = ""
    """The environment variable to use for this option"""

    key: str = ""
    """The key used for this option in the config file.

    This is the fully qualified key, e.g. "object-server.port" corresponds to the following yaml:
    ```yaml
    object-server:
        port: 5015
    ```

    """

    argument: str = ""
    """The command line argument for this option"""

    data_type: Any = None
    """The type of the option's value"""

    required: bool = False
    """Whether this option is required or not"""

    validate_func: Callable[[Any], bool] | None = None
    """A function to validate the value of this option"""

    transform_func: Callable[[Any], Any] | None = None
    """A function to transform the value of this option before reading it.

    The use case for this is e.g. to expand environment variables or do shell expansion in the value.
    """

    format_func: Callable[[Any], str | list[str]] = lambda x: x  # noqa: E731
    """A function to format the value for this option in serialization.

    This is useful for options that have complex values, such as lists or dictionaries.
    Default is identity.
    """

    @classmethod
    def class_from_key(cls, key: str) -> type[OPTION]:
        """Get the option class from a key.

        :param key: The key to look up, which should corresponds to the [](OPTION.key) attribute of an option class.
        :returns: The option class corresponding to the key.
        :raises RuntimeError: If the key does not corresponds to a valid option class.
        """
        subclass = [option_class for option_class in cls.__subclasses__() if option_class.key == key]

        if len(subclass) != 1:
            raise RuntimeError(f"Could not find option class for key {key}.")
        else:
            return subclass[0]

    @classmethod
    def is_hidden(cls) -> bool:
        """Whether this option should be hidden or not.

        :returns: True if this option should be hidden, False otherwise.
        """
        return cls.__name__.startswith("_")


class _API_KEY(OPTION):
    """API key to use."""

    default = ""
    key = "api_key"
    data_type = str
    envvar = "TLC_API_KEY"
    argument = "--api-key"


class OBJECT_SERVICE_PORT(OPTION):
    """Port for the server."""

    default = 5015
    key = "service.port"
    data_type = int
    transform_func = int
    envvar = "TLC_SERVICE_PORT"
    argument = "--port"


class OBJECT_SERVICE_HOST(OPTION):
    """Host for the server."""

    key = "service.host"
    envvar = "TLC_SERVICE_HOST"
    argument = "--host"
    default = "127.0.0.1"
    data_type = str


class OBJECT_SERVICE_LICENSE(OPTION):
    """Specify license or license file

    The option can be either be the license key or point to a local file containing the license key.
    """

    default = ""
    key = "service.license"
    envvar = "TLC_LICENSE"
    argument = "--license"
    data_type = str
    transform_func = lambda x: "" if x is None else str(x)  # noqa: E731


class OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE(OPTION):
    """Specify the amount of memory to use for caching, in bytes.

    Setting the value to 0 will disable in-memory caching.

    Default: 1073741824 (1 GB)
    """

    default = 1073741824
    key = "service.cache_in_memory_size"
    argument = "--cache-size"
    data_type = int


class OBJECT_SERVICE_CACHE_TIME_OUT(OPTION):
    """Specify the cache item time out, in seconds.

    Setting the value to 0 will disable cache eviction based on time.

    Default: 3600 (1 hour)
    """

    default = 3600
    key = "service.cache_time_out"
    argument = "--cache-time-out"
    data_type = int


class PROJECT_ROOT_URL_OPTION(OPTION):
    """Location for reading and writing 3LC data.

    This option is mandatory and must point to a location (e.g. directory on disk or object store bucket) with write
    access. The location will be created if it does not exist.

    If the option value contains an environment variable, it will be expanded.
    """

    default = os.path.join(get_default_root_dir(), "projects")
    """As returned by [](get_default_root_dir)"""

    key = "indexing.project-root-url"
    envvar = "TLC_CONFIG_PROJECT_ROOT_URL"
    argument = "--project-root-url"
    required = True
    data_type = str
    transform_func = _consider_expandvars
    validate_func = _ensure_dir_is_writeable


class PROJECT_SCAN_URLS_OPTION(OPTION):
    """Locations to scan for 3LC objects (runs and tables) following a standard 3LC project layout.

    The option value should be a list of URLs to scan for 3LC objects. Items in the list can be represented either by a
    string value (e.g., "s3://bucket") or as a dictionary with the required field 'url' and optional extra fields
    (e.g., {"url": "s3://bucket", "static": True}).

    Example values:
     - "C:\\Users\\user\\Documents\\3LC\\projects"
     - "s3://my-bucket/3LC/projects"
     - {"url": "s3://my-bucket/3LC/read-only-projects", "static": True}

    The only public optional field is 'static', which, when set to 'True', prevents the indexer from re-scanning
    the location.

    Each URL in this list is assumed to contain sub-projects. Default (sub-)directories will be created if they do
    not exist."""

    default = []
    key = "indexing.project-scan-urls"
    data_type = List[Union[str, Dict[str, Any]]]
    transform_func = partial(_dictify, key="url", inner=_consider_expandvars)

    # Format function to ensure that the output is as simplified as possible. Internal rep is dict, but use sub-field
    # (str) when sufficient.
    format_func = lambda lst: [  # noqa: E731
        x["url"] if (isinstance(x, dict) and list(x.keys()) == ["url"]) else x for x in lst
    ]


class EXTRA_TABLE_SCAN_URLS_OPTION(OPTION):
    """Extra (non-recursive) locations to scan for 3LC Table objects.

    This option allows searching individual folders/locations for 3LC Table objects outside the standard hierarchy of a
    3LC project structure. For example:
     - "C:\\Users\\user\\Documents\\3LC\\tables"
     - "s3://my-bucket/3LC/tables".

    Note: these locations will not be scanned recursively. See [](PROJECT_SCAN_URLS_OPTION) for details on URL options.

    Indexed Tables from these extra locations can be used interchangeably with other Tables discovered by the system.
    """

    default = []
    key = "indexing.extra-table-scan-urls"
    data_type = List[Union[str, Dict[str, Any]]]
    transform_func = partial(_dictify, key="url")
    # Format function to ensure that the output is as simplified as possible. Internal rep is dict, but use sub-field
    # (str) when sufficient.
    format_func = lambda lst: [  # noqa: E731
        x["url"] if (isinstance(x, dict) and list(x.keys()) == ["url"]) else x for x in lst
    ]


class EXTRA_RUN_SCAN_URLS_OPTION(OPTION):
    """Extra (non-recursive) locations to scan for 3LC Run objects.

    This option allows searching individual folders/locations for 3LC Run objects outside the standard hierarchy of a
    3LC project structure. For example:
     - "C:\\Users\\user\\Documents\\3LC\\runs"
     - "s3://my-bucket/3LC/runs".

    Note: these locations will not be scanned recursively. See [](PROJECT_SCAN_URLS_OPTION) for details on URL options.

    Indexed Runs from these extra locations can be used interchangeably with other Runs discovered by the system.
    """

    default = []
    key = "indexing.extra-run-scan-urls"
    data_type = List[Union[str, Dict[str, Any]]]
    transform_func = partial(_dictify, key="url")
    # Format function to ensure that the output is as simplified as possible. Internal rep is dict, but use sub-field
    # (str) when sufficient.
    format_func = lambda lst: [  # noqa: E731
        x["url"] if (isinstance(x, dict) and list(x.keys()) == ["url"]) else x for x in lst
    ]


class LOGFILE(OPTION):
    """Log file for the 3LC logger.

    The directory will be created if it does not exist.

    If the option value contains an environment variable, it will be expanded.
    """

    default = os.path.join(get_default_log_dir(), "3LC.log")
    """As returned by [](get_default_log_dir) / 3LC.log"""

    key = "logging.logfile"
    envvar = "TLC_LOGFILE"
    argument = "--logfile"
    data_type = str
    transform_func = _consider_expandvars
    validate_func = _ensure_file_is_writeable


class LOGLEVEL(OPTION):
    """Log level for the 3LC logger.

    The `tlc` Python package adheres to the standard Python logging levels:

      - DEBUG:  Detailed information, typically of interest only when diagnosing problems.
      - INFO: Confirmation that things are working as expected.
      - WARNING: An indication that something unexpected happened, or indicative of some problem in the near future
        (e.g. "disk space low"). The software is still working as expected.
      - ERROR: Due to a more serious problem, the software has not been able to perform some function.
      - CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
    """

    default = "WARNING"
    key = "logging.loglevel"
    envvar = "TLC_LOGLEVEL"
    argument = "--loglevel"
    data_type = str
    transform_func = str.upper
    validate_func = lambda x: x in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]  # noqa: E731


class DISPLAY_PROGRESS(OPTION):
    """Whether to display progress bars or not.

    The option can be either 0 or 1, where 0 means no progress bars and 1 means progress bars.
    """

    default = 1
    data_type = int
    transform_func = int
    key = "tlc.display-progress"
    envvar = "TLC_DISPLAY_PROGRESS"
    argument = "--display-progress"
    validate_func = lambda x: x in [0, 1]  # noqa: E731


class TELEMETRY(OPTION):
    """Whether to send Telemetry or not."""

    default = _get_default_telemetry()
    data_type = int
    key = "tlc.telemetry"
    envvar = "TLC_TELEMETRY"
    argument = "--telemetry"
    transform_func = int


class _SENTRY_OBJECT_SERVICE(OPTION):
    default = False
    data_type = bool
    key = "tlc.sentry-object-serivce"
    envvar = "TLC_SENTRY_OBJECT_SERVICE"


class ALIASES(OPTION):
    """List of registered aliases

    The option value should be a dictionary with the alias name as the key and the alias value as the value. In addition
    to the aliases in this list, the system will also consider 'data aliases' stored in special data configuration files
    and merge them with the aliases defined here.
    A data configuration file is a partial 3LC configuration that contains only one key: `aliases`. The system will look
    for such files, upon startup only, in the following locations:

       - `<PROJECT_SCAN_URL>/config.3lc.yaml` # top level
       - `<PROJECT_SCAN_URL>/<project_xyz>/config.3lc.yaml` # per project
       - `<EXTRA_TABLE_SCAN_URL>/config.3lc.yaml`
       - `<EXTRA_RUN_SCAN_URL>/config.3lc.yaml`

    ## Special alias syntax
    For aliases defined inside *data configuration files* it is possible to define an alias-value that is relative to
    the configuration file in which the alias is defined. This is done by prefixing the alias-value with `$.`, `$..` and
    so forth. The system will then expand the alias-value relative to the configuration file in which the alias is
    defined.

    ## Examples

    Example values (for all configuration files):
    ```
      PROJECT_XYZ_REMOTE_ALIAS: s3://my-bucket/3LC/projects/project-xyz
      PROJECT_XYZ_LOCAL_ALIAS: /home/user/projects/project-xyz
    ```

    Special syntax examples (only for data configuration files):
    ```
      PROJECT_XYZ_DATA_ALIAS: $./data # expands to the data directory relative to the configuration file itself
      PROJECT_XYZ_PARENT_DATA_ALIAS: $../data # relative to parent dir
      PROJECT_XYZ_PARENT_PARENT_DATA_ALIAS: $.../data # relative to parent's parent dir
    ```

    """

    default = {}
    data_type = Dict[str, str]
    key = "aliases"
    transform_func = _consider_expandvars


class _SERIALIZATION_CHECK_OVERRIDE(OPTION):
    """Whether to override the serialization check override."""

    default = False
    data_type = bool
    key = "tlc.serialization-check-override"
    transform_func = _any_to_bool
    envvar = "TLC_SERIALIZATION_CHECK_OVERRIDE"
