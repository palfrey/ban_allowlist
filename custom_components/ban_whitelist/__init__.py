"""The Ban Whitelist integration."""

from __future__ import annotations

import logging
from ipaddress import IPv4Address, IPv6Address
from typing import List

import voluptuous as vol
from homeassistant.components.http.ban import KEY_BAN_MANAGER, IpBanManager
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("ip_addresses"): vol.All(cv.ensure_list, [cv.string]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Ban Whitelist from a config entry."""
    ban_manager: IpBanManager = hass.http.app[KEY_BAN_MANAGER]
    _LOGGER.debug("Ban manager %s", ban_manager)
    whitelist: List[str] = config.get(DOMAIN, {}).get("ip_addresses", [])
    if len(whitelist) == 0:
        _LOGGER.info("Not setting whitelist, as no IPs set")
    else:
        _LOGGER.info("Setting whitelist with %s", whitelist)

        original_async_add_ban = IpBanManager.async_add_ban

        async def whitelist_async_add_ban(
            remote_addr: IPv4Address | IPv6Address,
        ) -> None:
            if str(remote_addr) in whitelist:
                _LOGGER.info(
                    "Not adding %s to ban list, as it's in the whitelist", remote_addr
                )
                return
            else:
                _LOGGER.info("Banning IP %s", remote_addr)

            await original_async_add_ban(ban_manager, remote_addr)

        ban_manager.async_add_ban = (  # type:ignore[method-assign]
            whitelist_async_add_ban  # type:ignore[assignment]
        )

    return True
