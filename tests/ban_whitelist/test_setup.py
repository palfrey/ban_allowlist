"""Test Ban Whitelist setup"""

import logging

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.loader import async_get_custom_components, DATA_CUSTOM_COMPONENTS

from custom_components.ban_whitelist.const import DOMAIN

@pytest.mark.anyio
async def test_setup(hass: HomeAssistant, caplog: pytest.LogCaptureFixture) -> None:
    hass.data[DATA_CUSTOM_COMPONENTS] = None
    assert list((await async_get_custom_components(hass)).keys()) == ["ban_whitelist"]
    await async_setup_component(hass, "http", {})
    await async_setup_component(hass, DOMAIN, {DOMAIN: {"ip_addresses": ["192.168.1.1"]}})

    for record in caplog.records:
        if record.levelno >= logging.WARNING:
            msg = record.getMessage()
            if msg.startswith("We found a custom integration ban_whitelist which has not been tested by Home Assistant"):
                continue
            raise Exception(record.getMessage())

