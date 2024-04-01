"""Test Ban Whitelist setup."""

import logging
from ipaddress import IPv4Address
from typing import cast

import pytest
from homeassistant.components.http.ban import KEY_BAN_MANAGER, IpBanManager
from homeassistant.core import HomeAssistant
from homeassistant.loader import DATA_CUSTOM_COMPONENTS, async_get_custom_components
from homeassistant.setup import async_setup_component

from custom_components.ban_whitelist.const import DOMAIN


def check_records(records: list[logging.LogRecord]) -> None:
    """Check log records don't have any warnings/errors."""
    for record in records:
        if record.levelno >= logging.WARNING:
            msg = record.getMessage()
            if msg.startswith(
                "We found a custom integration ban_whitelist which has not been tested by Home Assistant"
            ):
                continue
            raise Exception(msg)


async def setup_ban_whitelist(hass: HomeAssistant) -> None:
    """Configure ban_whitelist and dependencies."""
    hass.data[DATA_CUSTOM_COMPONENTS] = None
    assert list((await async_get_custom_components(hass)).keys()) == ["ban_whitelist"]
    await async_setup_component(hass, "http", {})
    await async_setup_component(
        hass, DOMAIN, {DOMAIN: {"ip_addresses": ["192.168.1.1"]}, "foo": "bar"}
    )


@pytest.mark.anyio
async def test_setup(hass: HomeAssistant, caplog: pytest.LogCaptureFixture) -> None:
    """Test setup of ban whitelist."""
    await setup_ban_whitelist(hass)
    check_records(caplog.records)


@pytest.mark.anyio
async def test_hit_whitelist(
    hass: HomeAssistant, caplog: pytest.LogCaptureFixture
) -> None:
    """Test hitting the whitelist."""
    await setup_ban_whitelist(hass)
    await cast(IpBanManager, hass.http.app[KEY_BAN_MANAGER]).async_add_ban(
        IPv4Address("192.168.1.1")
    )
    await cast(IpBanManager, hass.http.app[KEY_BAN_MANAGER]).async_add_ban(
        IPv4Address("10.0.0.1")
    )
    check_records(caplog.records)

    messages = []

    for record in caplog.records:
        if record.levelno < logging.INFO or not record.name.startswith(
            "custom_components.ban_whitelist"
        ):
            continue

        messages.append(record.getMessage())

    assert messages == [
        "Setting whitelist with ['192.168.1.1']",
        "Not adding 192.168.1.1 to ban list, as it's in the whitelist",
        "Banning IP 10.0.0.1",
    ]
