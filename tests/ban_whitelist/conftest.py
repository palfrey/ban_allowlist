"""Common fixtures for the Ban Whitelist tests."""

import pytest


@pytest.fixture
def anyio_backend():
    """Config anyio with asyncio (as that's what HA uses)."""
    return "asyncio"
