"""Integration tests for FeedsClient."""

from pathlib import Path
from typing import Callable

import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.feeds import FeedsClient
from nisystemlink.clients.feeds.models import CreateFeedRequest, Platform


WINDOWS_FEED_NAME = "Windows feed"
LINUX_FEED_NAME = "Linux feed"
FEED_DESCRIPTION = "Sample feed for uploading packages"
INVALID_WORKSPACE_ID = "12345"
PACKAGE_PATH = (
    Path(__file__).parent.resolve()
    / "test_files"
    / "sample-measurement_0.5.0_windows_x64.nipkg"
)
INVALID_PACKAGE_PATH = Path(__file__).parent.resolve()


@pytest.fixture(scope="class")
def client(enterprise_config) -> FeedsClient:
    """Fixture to create a FeedsClient instance."""
    return FeedsClient(enterprise_config)


@pytest.fixture(scope="class")
def create_feed(client: FeedsClient):
    """Fixture to return a object that creates feed."""

    def _create_feed(feed):
        response = client.create_feed(feed)
        return response

    yield _create_feed


@pytest.fixture(scope="class")
def create_windows_feed_request():
    """Fixture to create a request body of create feed API for windows platform."""

    def _create_feed_request():
        feed_request = CreateFeedRequest(
            name=WINDOWS_FEED_NAME,
            platform=Platform.WINDOWS.value,
            description=FEED_DESCRIPTION,
        )
        return feed_request

    yield _create_feed_request


@pytest.fixture(scope="class")
def create_linux_feed_request():
    """Fixture to create a request body of create feed API for linux platform."""

    def _create_feed_request():
        feed_request = CreateFeedRequest(
            name=LINUX_FEED_NAME,
            platform=Platform.NI_LINUX_RT.value,
            description=FEED_DESCRIPTION,
        )
        return feed_request

    yield _create_feed_request


@pytest.fixture(scope="class")
def get_windows_feed_id(client: FeedsClient):
    """Fixture to return the Feed ID of the created windows feed."""
    query_feeds_response = client.query_feeds(platform=Platform.WINDOWS.value)

    for feed in query_feeds_response.feeds:
        if feed.name == WINDOWS_FEED_NAME:
            return feed.id


@pytest.fixture(scope="class")
def get_linux_feed_id(client: FeedsClient):
    """Fixture to return the Feed ID of the created Linux feed."""
    query_feeds_response = client.query_feeds(platform=Platform.NI_LINUX_RT.value)

    for feed in query_feeds_response.feeds:
        if feed.name == LINUX_FEED_NAME:
            return feed.id


@pytest.mark.enterprise
@pytest.mark.integration
class TestFeedsClient:
    """Class contains a set of test methods to test SystemLink Feeds API."""

    def test__create_feed_windows_platform(
        self,
        create_feed: Callable,
        create_windows_feed_request: Callable,
    ):
        """Test the case of a completely successful create feed API for windows platform."""
        request_body = create_windows_feed_request()
        response = create_feed(request_body)

        assert response.id is not None
        assert response.workspace is not None
        assert response.name == WINDOWS_FEED_NAME
        assert response.platform == Platform.WINDOWS
        assert response.description == FEED_DESCRIPTION

    def test__create_feed_linux_platform(
        self,
        create_feed: Callable,
        create_linux_feed_request: Callable,
    ):
        """Test the case of a completely successful create feed API for Linux platform."""
        request_body = create_linux_feed_request()
        response = create_feed(request_body)

        assert response.id is not None
        assert response.workspace is not None
        assert response.name == LINUX_FEED_NAME
        assert response.platform == Platform.NI_LINUX_RT
        assert response.description == FEED_DESCRIPTION

    def test__query_feeds_windows_platform(self, client: FeedsClient):
        """Test the case for querying available feeds for windows platform."""
        response = client.query_feeds(platform=Platform.WINDOWS.value)
        assert response is not None

    def test__query_feeds_linux_platform(self, client: FeedsClient):
        """Test the case for querying available feeds for linux platform."""
        response = client.query_feeds(platform=Platform.NI_LINUX_RT.value)
        assert response is not None

    def test__query_feeds_invalid_workspace(self, client: FeedsClient):
        """Test the case of query feeds API with invalid workspace id."""
        with pytest.raises(ApiException, match="UnauthorizedWorkspaceError"):
            client.query_feeds(workspace=INVALID_WORKSPACE_ID)

    def test__upload_package(self, client: FeedsClient, get_windows_feed_id: str):
        """Test the case of upload package to feed."""
        response = client.upload_package(
            package=open(PACKAGE_PATH, "rb"),
            feed_id=get_windows_feed_id,
            overwrite=True,
        )
        assert response is not None

    def test__upload_duplicate_package(
        self,
        client: FeedsClient,
        get_windows_feed_id: str,
    ):
        """Test the case of uploading duplicate package to feed."""
        with pytest.raises(ApiException, match="DuplicatePackageError"):
            client.upload_package(
                package=open(PACKAGE_PATH, "rb"),
                feed_id=get_windows_feed_id,
            )

    def test__delete__windows_feed(self, client: FeedsClient, get_windows_feed_id: str):
        """Test the case of deleting windows feed with its packages."""
        response = client.delete_feed(feed_id=get_windows_feed_id)
        assert response is None

    def test__delete__linux_feed(self, client: FeedsClient, get_linux_feed_id: str):
        """Test the case of deleting linux feed with its packages."""
        response = client.delete_feed(feed_id=get_linux_feed_id)
        assert response is None
