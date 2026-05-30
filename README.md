# Home Assistant IP Ban Allowlist plugin

Status: **Maintained compatibility integration**

[![Add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=palfrey&repository=ban_allowlist&category=integration)

Home Assistant has [a very useful IP banning feature](https://www.home-assistant.io/integrations/http/#ip-filtering-and-banning) which is nice for when you've got a private but externally facing instance that you'd like to reduce the odds on getting hacked.

However, it's got one little missing feature: IP allowlists. Without this, sometimes you get the problem that your home IP gets banned (because you've got something internal to your house using the external naming), which is a bit frustrating. The position of the core devs appears to be ["this is a bug with something else that we shouldn't workaround"](https://github.com/home-assistant/core/pull/52334), but meanwhile we're stuck with the banning happening every so often.

This integration fills that gap by adding an allowlist check around Home Assistant's IP ban handling, so trusted addresses and networks can avoid being added to `ip_bans.yaml`.

This integration has a unit test suite and is explicitly integration tested against every latest patch version of HA from 2025.1.4 up (i.e. for every `x.y.z` version, we test all values of `x.y` using the latest `z` value). It depends on Home Assistant's internal HTTP ban handling, so review release notes and test after major Home Assistant upgrades.

## Installation

Use the button above to add this repository to HACS, then install **IP Ban Allowlist** from HACS and restart Home Assistant.

If the button does not work, add it manually in HACS:

1. Open HACS.
2. Open the three-dot menu and choose **Custom repositories**.
3. Add `https://github.com/palfrey/ban_allowlist`.
4. Choose the **Integration** category.
5. Install **IP Ban Allowlist** and restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & services**.
2. Select **Add integration**.
3. Search for **IP Ban Allowlist**.
4. Enter trusted IP addresses or CIDR networks, one per line.

Example entries:

```text
192.168.1.10
192.168.1.0/24
2001:db8::/64
```

You can update the allowlist later from the integration's **Configure** button.

## Migrating from YAML

Older versions used `configuration.yaml`:

```yaml
ban_allowlist:
  ip_addresses:
    - 192.168.1.10
    - 192.168.1.0/24
```

This format is still imported for compatibility. After Home Assistant creates the config entry, remove the YAML block and manage the allowlist from the UI.
