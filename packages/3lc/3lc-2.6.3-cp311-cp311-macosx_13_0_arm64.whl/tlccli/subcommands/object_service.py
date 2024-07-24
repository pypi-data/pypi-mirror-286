# =============================================================================
# <copyright>
# Copyright (c) 2023 3LC Inc. All rights reserved.
#
# All rights are reserved. Reproduction or transmission in whole or in part, in
# any form or by any means, electronic, mechanical or otherwise, is prohibited
# without the prior written permission of the copyright owner.
# </copyright>
# =============================================================================
"""Subcommand for the service command."""

from __future__ import annotations

import argparse
import asyncio
import atexit
import os
import platform
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Generator
from urllib.parse import urlencode, urlparse, urlunparse

import rich
import rich.tree
import sentry_sdk
import starlite
import tlcconfig.options as options
import uvicorn
from starlite.types.callable_types import LifeSpanHookHandler
from tlcconfig.option_loader import OptionLoader
from tlcconfig.version import _PACKAGE_VERSION
from tlcsaas.key_utils import is_license_key

from tlccli.subcommand import SubCommand
from tlccli.subcommands.ngrok_helper import NGrokHelper
from tlccli.subcommands.object_service_tui import ObjectServiceTUI


class ObjectServiceSubCommand(SubCommand):
    """Handle the service sub-command."""

    key = "service"

    def __init__(
        self,
        subparser: argparse._SubParsersAction[argparse.ArgumentParser],
    ) -> None:
        super().__init__(ObjectServiceSubCommand.key, subparser)
        self.parser = self.create_subparser(subparser)

    @staticmethod
    def is_terminal_interactive() -> bool:
        is_interactive = sys.stdout.isatty() and sys.stdin.isatty()
        return is_interactive

    def create_subparser(
        self,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ) -> argparse.ArgumentParser:
        parser = subparsers.add_parser(
            ObjectServiceSubCommand.key,
            help="""Start the service.
            Run with `service --help` for more details.""",
        )
        parser.add_argument(
            "--host",
            type=str,
            help="The host address to bind to.",
            default=OptionLoader.instance().get_value(options.OBJECT_SERVICE_HOST),
        )
        parser.add_argument(
            "--port",
            type=int,
            help="The port to bind to.",
            default=OptionLoader.instance().get_value(options.OBJECT_SERVICE_PORT),
        )
        parser.add_argument(
            "--no-public-examples",
            action="store_true",
            help="Do not include the 3LC public examples in the service.",
            default=False,
        )

        parser.add_argument(
            "--dashboard",
            action="store_true",
            help="Whether to try to automatically open a browser to the Dashboard once the Object Service is running.",
            default=False,
        )

        parser.add_argument(
            "--ngrok",
            action="store_true",
            help=(
                "Set up a public URL using NGrok. This will expose the service to the internet. "
                "Using this feature requires a valid NGrok token set in the NGROK_TOKEN environment variable."
            ),
            default=False,
        )

        tui_group = parser.add_mutually_exclusive_group()

        if sys.version_info >= (3, 9):
            tui_group.add_argument(
                "--tui",
                action=argparse.BooleanOptionalAction,
                help=(
                    "Show a full screen terminal application for the Object Service, "
                    "this is the default when using an interactive terminal. Use --no-tui to disable."
                ),
                default=ObjectServiceSubCommand.is_terminal_interactive(),
            )
        else:
            tui_group.add_argument(
                "--tui",
                action="store_true",
                help=(
                    "Show a full screen terminal application for the Object Service, "
                    "this is the default when using an interactive terminal. Use --no-tui to disable."
                ),
                default=ObjectServiceSubCommand.is_terminal_interactive(),
            )
            tui_group.add_argument(
                "--no-tui",
                action="store_false",
                dest="tui",
                help="Disable the full screen terminal application for the Object Service.",
            )

        parser.add_argument(
            options.OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE.argument,
            type=options.OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE.data_type,
            help=options.OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE.__doc__,
            default=OptionLoader.instance().get_value(options.OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE),
        )

        parser.add_argument(
            options.OBJECT_SERVICE_CACHE_TIME_OUT.argument,
            type=options.OBJECT_SERVICE_CACHE_TIME_OUT.data_type,
            help=options.OBJECT_SERVICE_CACHE_TIME_OUT.__doc__,
            default=OptionLoader.instance().get_value(options.OBJECT_SERVICE_CACHE_TIME_OUT),
        )

        return parser

    def handle_command(self, args: argparse.Namespace) -> int:
        OptionLoader.instance().set_value(
            options._SENTRY_OBJECT_SERVICE,
            True,
        )

        if args.ngrok:
            if not NGrokHelper.is_pyngrok_available():
                self.parser.error(NGrokHelper.pyngrok_unavailable_message)

            if not NGrokHelper.is_ngrok_token_available():
                self.parser.error(NGrokHelper.ngrok_token_unavailable_message)

        # set default based on parsed args, if not specified, default sets to default (nop)
        # this allows us to pull out parsed args anywhere
        OptionLoader.instance().set_value(options.OBJECT_SERVICE_CACHE_IN_MEMORY_SIZE, args.cache_size)
        OptionLoader.instance().set_value(options.OBJECT_SERVICE_CACHE_TIME_OUT, args.cache_time_out)

        launch_object_service(
            host=args.host,
            port=args.port,
            with_public_examples=not args.no_public_examples,
            dashboard=args.dashboard,
            ngrok=args.ngrok,
            tui=args.tui,
        )
        return 0


@contextmanager
def _run_object_service(
    host: str,
    port: int,
    with_public_examples: bool,
    ngrok: bool,
    tui: bool,
    dashboard: bool,
    starlite_after_startup_handler: LifeSpanHookHandler | None = None,
    starlite_after_shutdown_handler: LifeSpanHookHandler | None = None,
) -> Generator[uvicorn.Server, None, None]:
    from tlc.service import object_service  # Triggers creation of global objects  # noqa: I001
    from tlc.core.utils.telemetry import _add_object_service_lru_cache_info, RunningMessage
    from tlc.core.utils.track_project_metadata import get_project_usage_metadata

    if with_public_examples:
        configure_public_examples()

    session_id = str(uuid.uuid4())
    start_time = datetime.now(timezone.utc)
    running_message = RunningMessage(session_id, start_time)

    app = object_service.create_starlite_app(
        host,
        port,
        ngrok,
        dashboard,
        starlite_after_startup_handler,
        starlite_after_shutdown_handler,
    )

    config = uvicorn.Config(
        app,
        port=port,
        host=host,
        # The uvicorn log level does not correspond to our (not the Python standard) log levels.
        log_level="warning",
        timeout_keep_alive=60,
        callback_notify=running_message.consider_message,
    )

    with sentry_sdk.configure_scope() as scope:
        scope.clear_breadcrumbs()
        scope.set_tag("mode", "tui" if tui else "no-tui")
        scope.set_tag("public_examples", with_public_examples)
        scope.set_tag("ngrok", ngrok)
        scope.set_tag("session_id", session_id)
        scope.set_extra("start_time", start_time)
        _add_object_service_lru_cache_info(scope, include_stats=False)
        sentry_sdk.capture_message("Object Service: Start", level="info")
    sentry_sdk.flush()

    is_sent_object_service_stop_message = False

    def send_object_service_stop_message(is_exit_on_error: bool) -> None:
        nonlocal is_sent_object_service_stop_message
        assert not is_sent_object_service_stop_message
        is_sent_object_service_stop_message = True
        end_time = datetime.now(timezone.utc)
        elapsed_time = (end_time - start_time).total_seconds()
        with sentry_sdk.configure_scope() as scope:
            scope.clear_breadcrumbs()
            scope.set_tag("mode", "no-tui")
            scope.set_tag("public_examples", with_public_examples)
            scope.set_tag("ngrok", ngrok)
            scope.set_tag("session_id", session_id)
            scope.set_tag("is_exit_on_error", is_exit_on_error)
            scope.set_extra("start_time", start_time)
            scope.set_extra("end_time", end_time)
            scope.set_extra("elapsed_time", elapsed_time)
            scope.set_extra("project_stats", get_project_usage_metadata())
            _add_object_service_lru_cache_info(scope, include_stats=True)
            sentry_sdk.capture_message("Object Service: Stop", level="info")
        sentry_sdk.flush()

    uvicorn_server = uvicorn.Server(config)

    # It is possible for uvicorn to call sys.exit, in which case we need an atexit handler in place to ensure that the
    # stop message is sent.
    atexit.register(send_object_service_stop_message, True)
    yield uvicorn_server
    atexit.unregister(send_object_service_stop_message)

    send_object_service_stop_message(False)


def launch_object_service(
    host: str, port: int, with_public_examples: bool, dashboard: bool, ngrok: bool, tui: bool
) -> None:
    """Launch the object service, fetching the configuration from the OptionLoader."""

    if host != options.OBJECT_SERVICE_HOST().default:
        OptionLoader.instance().set_value(options.OBJECT_SERVICE_HOST, host)
    else:
        host = OptionLoader.instance().get_value(options.OBJECT_SERVICE_HOST)
    if port != options.OBJECT_SERVICE_PORT().default:
        OptionLoader.instance().set_value(options.OBJECT_SERVICE_PORT, port)
    else:
        port = OptionLoader.instance().get_value(options.OBJECT_SERVICE_PORT)

    # log_level = TLCOptionLoader.instance().get(options.LOGLEVEL)

    if tui:
        # Force resolution of API key here.
        # If the API key is not set or not valid, we prompt the user to enter the API key via a call to input. That does
        # not work when using the TUI.
        from tlcsaas.key_utils import ensure_key_activated

        ensure_key_activated()

        tui_app = ObjectServiceTUI(
            host=host,
            port=port,
            ngrok=ngrok,
            public_examples=with_public_examples,
            dashboard=dashboard,
        )
        tui_app.run()
    else:
        from tlc.service.object_service import StarliteStateConstants  # noqa: I001

        platform_string = f"{platform.system()} {platform.version()} ({platform.machine()})"

        print(f"3LC Object Service - Version: {_PACKAGE_VERSION}, PID: {os.getpid()} (Use Ctrl-C to exit.)")
        print(f"Platform: {platform_string}, Python: {platform.python_version()}")

        def after_object_service_startup_handler(starlite: starlite.Starlite) -> None:
            if starlite.state[StarliteStateConstants.OBJECT_SERVICE_RUNNING_URLS]:
                url_or_urls = (
                    "URLs" if len(starlite.state[StarliteStateConstants.OBJECT_SERVICE_RUNNING_URLS]) > 1 else "URL"
                )

                tree = rich.tree.Tree(f"Object Service {url_or_urls}:")

                for url in starlite.state[StarliteStateConstants.OBJECT_SERVICE_RUNNING_URLS]:
                    tree.add(url)

                rich.print(tree)

            dashboard_urls = get_effective_dashboard_urls(starlite.state)

            if dashboard_urls:
                url_or_urls = "URLs" if len(dashboard_urls) > 1 else "URL"
                tree = rich.tree.Tree(f"Dashboard {url_or_urls}:")

                for url in dashboard_urls:
                    tree.add(url)

                rich.print(tree)

        with _run_object_service(
            host=host,
            port=port,
            with_public_examples=with_public_examples,
            ngrok=ngrok,
            tui=False,
            dashboard=dashboard,
            starlite_after_startup_handler=after_object_service_startup_handler,
        ) as uvicorn_server:
            try:
                uvicorn_server.run()
            except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
                # This is the expected path when exiting the application using Ctrl-C
                pass


def get_effective_dashboard_urls(state: starlite.State) -> list[str]:
    """Return the effective dashboard URL.

    This method parses a dict created during Starlite initialization, and returns the effective dashboard URL
    that the user should use to access the dashboard.
    """

    if is_license_key():
        return []

    from tlc.service.object_service import StarliteStateConstants
    from tlcsaas.runtime_config import DASHBOARD_URL

    query_parameters: list[str] = []

    # If NGrok is enabled, we assume that is the only interesting URL to show.
    if ngrok_object_service_url := state.get(StarliteStateConstants.NGROK_OBJECT_SERVICE_URL):
        query_parameters.append(urlencode({"object_service": ngrok_object_service_url}))
    elif object_service_running_urls := state.get(StarliteStateConstants.OBJECT_SERVICE_RUNNING_URLS):
        default_dashboard_url = f"http://{options.OBJECT_SERVICE_HOST.default}:{options.OBJECT_SERVICE_PORT.default}"

        for url in object_service_running_urls:
            if url == default_dashboard_url:
                # Do not set up a query parameter for the default port and make it be the first one we display.
                query_parameters.insert(0, "")
            else:
                query_parameters.append(urlencode({"object_service": url}))

    t = urlparse(DASHBOARD_URL)
    scheme = t.scheme  # type: ignore
    dashboard_netloc = t.netloc  # type: ignore

    urls = []

    for query_parameter in query_parameters:
        url = urlunparse((scheme, dashboard_netloc, "", "", query_parameter, ""))
        urls.append(url)

    # We always want to show the dashboard URL if we can't present any other url.
    # The will also ensure that we will print the URL if the Object Service in only running on the default localhost.
    if len(urls) == 0:
        urls.append(DASHBOARD_URL)

    return urls


def configure_public_examples() -> None:
    """Configure the object service to serve the public examples.

    For the samples to work out-of-the-box, the public examples table/root urls must be indexed, and a project-level
    alias must be created for each of the public examples.
    """
    from tlc.client.utils import (
        _TLC_PUBLIC_EXAMPLES_BALLOONS_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_BALLOONS_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_BALLOONS_MASK_SEGMENTATION_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_BALLOONS_MASK_SEGMENTATION_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_CIFAR_10_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_CIFAR_10_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_CIFAR_100_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_CIFAR_100_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_COCO_128_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_COCO_128_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_MNIST_DATA_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_MNIST_DATA_ALIAS_VALUE,
        _TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_NAME,
        _TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_VALUE,
    )
    from tlc.core.objects.tables.system_tables.indexing_tables import RunIndexingTable, TableIndexingTable
    from tlc.core.objects.tables.system_tables.indexing_tables.config_indexing_table import ConfigIndexingTable
    from tlc.core.url import Url, UrlAliasRegistry

    # Extend scan URLs, and set a large timeout to avoid unnecessary scans of static data
    TableIndexingTable.instance().add_scan_url(
        {
            "url": Url(_TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_VALUE),
            "layout": "project",
            "interval": 60.0 * 60 * 24,
            "object_type": "table",
            "static": True,
        }
    )

    RunIndexingTable.instance().add_scan_url(
        {
            "url": Url(_TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_VALUE),
            "layout": "project",
            "interval": 60.0 * 60 * 24,
            "object_type": "run",
            "static": True,
        }
    )
    ConfigIndexingTable.instance().add_scan_url(
        {
            "url": Url(_TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_VALUE),
            "layout": "project",
            "interval": 60.0 * 60 * 24,
            "object_type": "config",
            "static": True,
        }
    )

    # Register project root alias
    if _TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_PROJECT_ROOT_ALIAS_VALUE,
        )

    # Register MNIST data alias
    if _TLC_PUBLIC_EXAMPLES_MNIST_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_MNIST_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_MNIST_DATA_ALIAS_VALUE,
        )

    # Register CIFAR-10 data alias
    if _TLC_PUBLIC_EXAMPLES_CIFAR_10_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_CIFAR_10_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_CIFAR_10_DATA_ALIAS_VALUE,
        )

    # Register CIFAR-100 data alias
    if _TLC_PUBLIC_EXAMPLES_CIFAR_100_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_CIFAR_100_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_CIFAR_100_DATA_ALIAS_VALUE,
        )

    # Register COCO-128 data alias
    if _TLC_PUBLIC_EXAMPLES_COCO_128_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_COCO_128_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_COCO_128_DATA_ALIAS_VALUE,
        )

    # Register Balloons data alias
    if _TLC_PUBLIC_EXAMPLES_BALLOONS_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_BALLOONS_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_BALLOONS_DATA_ALIAS_VALUE,
        )

    # Register Balloons Mask Segmentation data alias
    if _TLC_PUBLIC_EXAMPLES_BALLOONS_MASK_SEGMENTATION_DATA_ALIAS_NAME not in UrlAliasRegistry.instance():
        UrlAliasRegistry.instance().register_url_alias(
            _TLC_PUBLIC_EXAMPLES_BALLOONS_MASK_SEGMENTATION_DATA_ALIAS_NAME,
            _TLC_PUBLIC_EXAMPLES_BALLOONS_MASK_SEGMENTATION_DATA_ALIAS_VALUE,
        )
