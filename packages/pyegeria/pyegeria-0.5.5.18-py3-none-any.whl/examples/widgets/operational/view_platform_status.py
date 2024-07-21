#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Display the status of cataloged platforms and servers.
"""

import time
import argparse
import os

from pyegeria._exceptions import (
    InvalidParameterException,
    PropertyServerException,
    UserNotAuthorizedException,
    print_exception_response,
)
from rich.table import Table
from rich.live import Live
from rich.console import Console

from pyegeria import RuntimeManager

EGERIA_KAFKA_ENDPOINT = os.environ.get('KAFKA_ENDPOINT', 'localhost:9092')
EGERIA_PLATFORM_URL = os.environ.get('EGERIA_PLATFORM_URL', 'https://localhost:9443')
EGERIA_VIEW_SERVER = os.environ.get('VIEW_SERVER', 'view-server')
EGERIA_VIEW_SERVER_URL = os.environ.get('EGERIA_VIEW_SERVER_URL', 'https://localhost:9443')
EGERIA_INTEGRATION_DAEMON = os.environ.get('INTEGRATION_DAEMON', 'integration-daemon')
EGERIA_ADMIN_USER = os.environ.get('ADMIN_USER', 'garygeeke')
EGERIA_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'secret')
EGERIA_USER = os.environ.get('EGERIA_USER', 'erinoverview')
EGERIA_USER_PASSWORD = os.environ.get('EGERIA_USER_PASSWORD', 'secret')


disable_ssl_warnings = True
console = Console(width=200)

def display_status(server: str, url: str, username: str):
    r_client = RuntimeManager(server, url, username)
    token = r_client.create_egeria_bearer_token(username, "secret")
    def generate_table() -> Table:
        """Make a new table."""
        table = Table(
            title=f"Server Status for Platform - {time.asctime()}",
            # style = "black on grey66",
            header_style="white on dark_blue",
            caption=f"Status of Platforms - '{url}'",
            show_lines=True,
            # expand=True
        )
        table.add_column("Platform Name")
        # table.add_column("Platform GUID")
        table.add_column("Platform URL")
        table.add_column("Platform Origin")
        table.add_column("Description")
        table.add_column("Platform Started")
        table.add_column("Servers")

        server_types = {
            "Metadata Access Store": "Store",
            "View Server" : "View",
            "Engine Host Server" : "EngineHost",
            "Integration Daemon" : "Integration"
        }

        platform_list = r_client.get_platforms_by_type()
        for platform in platform_list:
            platform_name = platform['properties']["name"]
            platform_guid = platform['elementHeader']["guid"]
            platform_desc = platform['properties']["description"]
            server_list = ""
            try:
                platform_report = r_client.get_platform_report(platform_guid)
                platform_url = platform_report.get('platformURLRoot'," ")
                platform_origin = platform_report.get("platformOrigin"," ")
                platform_started = platform_report.get("platformStartTime"," ")

                servers = platform_report.get("omagservers",None)

                if servers is not None:
                    for server in servers:
                        server_name = server.get("serverName"," ")
                        server_type = server.get("serverType"," ")
                        server_status = server.get("serverActiveStatus","UNKNOWN")
                        if server_status in("RUNNING", "STARTING"):
                            status_flag = "[green]"
                        elif server_status in ("INACTIVE", "STOPPING"):
                            status_flag = "[red]"
                        else:
                            server_status = "UNKNOWN"
                            status_flag = "[yellow]"

                        serv = f"{status_flag}{server_types[server_type]}: {server_name}\n"
                        server_list = server_list + serv

            except (Exception) as e:
                # console.print_exception(e)
                platform_url = " "
                platform_origin = " "
                platform_started = " "

            table.add_row(platform_name, platform_url, platform_origin, platform_desc,
                         platform_started, server_list)


        return table


    try:
        with Live(generate_table(), refresh_per_second=4, screen=True) as live:
            while True:
                time.sleep(2)
                live.update(generate_table())

    except (InvalidParameterException, PropertyServerException, UserNotAuthorizedException) as e:
        print_exception_response(e)


    finally:
        r_client.close_session()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="Name of the server to display status for")
    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    server = args.server if args.server is not None else EGERIA_VIEW_SERVER
    url = args.url if args.url is not None else EGERIA_PLATFORM_URL
    userid = args.userid if args.userid is not None else EGERIA_USER

    display_status(server, url, userid)


if __name__ == "__main__":
    main()