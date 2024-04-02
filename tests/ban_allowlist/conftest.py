"""Common fixtures for the Ban Allowlist tests."""

import pytest


@pytest.fixture
def anyio_backend():
    """Config anyio with asyncio (as that's what HA uses)."""
    return "asyncio"
