"""Common fixtures for the Ban Whitelist tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def anyio_backend():
    return 'asyncio'