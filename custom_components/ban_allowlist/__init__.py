"""The Ban Allowlist integration."""

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
    """Set up Ban Allowlist from a config entry."""
    try:
        ban_manager: IpBanManager = hass.http.app[KEY_BAN_MANAGER]
    except KeyError:
        _LOGGER.warn(
            "Can't find ban manager. ban_allowlist requires http.ip_ban_enabled to be True, so disabling."
        )
        return True
    _LOGGER.debug("Ban manager %s", ban_manager)
    allowlist: List[str] = config.get(DOMAIN, {}).get("ip_addresses", [])
    if len(allowlist) == 0:
        _LOGGER.info("Not setting allowlist, as no IPs set")
    else:
        _LOGGER.info("Setting allowlist with %s", allowlist)

        original_async_add_ban = IpBanManager.async_add_ban

        async def allowlist_async_add_ban(
            remote_addr: IPv4Address | IPv6Address,
        ) -> None:
            if str(remote_addr) in allowlist:
                _LOGGER.info(
                    "Not adding %s to ban list, as it's in the allowlist", remote_addr
                )
                return
            else:
                _LOGGER.info("Banning IP %s", remote_addr)

            await original_async_add_ban(ban_manager, remote_addr)

        ban_manager.async_add_ban = (  # type:ignore[method-assign]
            allowlist_async_add_ban
        )

    return True
