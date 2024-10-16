"""Helper functions for using systemlink feeds APIs."""

import os
from typing import List, Union

from nisystemlink.clients.auth import AuthClient
from nisystemlink.clients.core import ApiException, HttpConfiguration
from nisystemlink.clients.feeds.feeds_client import SystemLinkFeedsClient
from nisystemlink.clients.feeds.models import (
    CreateFeedRequest,
    CreateOrUpdateFeedResponse,
    Platform,
)
NIPKG = ".nipkg"


def __get_feed_platform(package_path: str) -> str:
    _, pkg_ext = os.path.splitext(package_path)

    if pkg_ext == NIPKG:
        return Platform.WINDOWS.value

    return Platform.NI_LINUX_RT.value


def __get_workspace_id(
    workspace_name: str, server_api_key: str, server_url: str,
) -> Union[str, None]:
    auth_client = AuthClient(HttpConfiguration(server_uri=server_url, api_key=server_api_key))
    caller_info = auth_client.authenticate()
    workspaces_info = caller_info.workspaces

    for workspace_info in workspaces_info:
        if workspace_info.name == workspace_name:
            return workspace_info.id


def create_feed(
    feed_name: str,
    platform: str,
    workspace_id: str,
    client: SystemLinkFeedsClient
) -> CreateOrUpdateFeedResponse:
    """Create new feed in systemlink.

    Args:
        feed_name (str): Name of the feed.
        platform (str): Name of the platform.
        workspace_id (str): Workspace ID.
        client (SystemLinkFeedsClient): Systemlink feeds Client.

    Returns:
        CreateOrUpdateFeedResponse: Create feed response.
    """
    create_feed_request = CreateFeedRequest(
        name=feed_name,
        workspace=workspace_id,
        platform=platform,
    )
    create_feed_response = client.create_feed(create_feed_request)
    return create_feed_response


def upload_single_package(
    package_path: str,
    workspace_name: str,
    server_api_key: str,
    server_url: str,
    feed_name: str,
    overwrite: bool,
) -> str:
    """Upload package to `SystemLink` feeds.

    Args:
        package_path (str): Path of the package file.
        workspace_name (str): Workspace name.
        server_api_key (str): Systemlink API Key.
        server_url (str): Systemlink API URL.
        feed_name (str): Name of the feed.
        overwrite (bool): To overwrite the package if exists. Defaults to false.

    Returns:
        str: Upload package response.
    """
    try:
        platform = __get_feed_platform(package_path)
        client = SystemLinkFeedsClient(
            HttpConfiguration(api_key=server_api_key, server_uri=server_url)
        )
        workspace_id = __get_workspace_id(
            workspace_name=workspace_name,
            server_api_key=server_api_key,
            server_url=server_url,
        )

        query_feeds = client.query_feeds(
            platform=platform,
            workspace=workspace_id,
        )
        existing_feeds = {}
        for feed in query_feeds.feeds:
            existing_feeds[feed.name] = feed.id

        if feed_name not in existing_feeds:
            feed_id = create_feed(
                feed_name=feed_name,
                workspace_id=workspace_id,
                client=client,
                platform=platform,
            )
        else:
            feed_id = existing_feeds[feed_name]

        package_name = os.path.basename(package_path)
        response = client.upload_package(
            feed_id=feed_id,
            package=(package_name, open(package_path, "rb"), "multipart/form-data"),
            overwrite=overwrite,
        )

        return response.file_name

    except (ApiException, Exception) as exp:
        return exp.message


def upload_multiple_packages(
    package_paths: List[str],
    workspace_name: str,
    server_api_key: str,
    server_url: str,
    feed_name: str,
    overwrite: bool,
) -> str:
    """Upload multiple packages to systemlink feeds.

    Args:
        package_paths (List[str]): List of package file paths.
        workspace_name (str): Workspace name.
        server_api_key (str): Systemlink API Key.
        server_url (str): Systemlink API URL.
        feed_name (str): Name of the feed.
        overwrite (bool): To overwrite the package if exists.

    Returns:
        str: Upload package responses.
    """
    failed_packages = []
    for package_path in package_paths:
        try:
            upload_single_package(
                package_path=package_path,
                server_api_key=server_api_key,
                server_url=server_url,
                workspace_name=workspace_name,
                overwrite=overwrite,
                feed_name=feed_name,
            )

        except (ApiException, Exception) as exp:
            failed_packages.append(exp.message)

    return failed_packages