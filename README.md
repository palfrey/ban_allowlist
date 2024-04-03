# Home Assistant IP Ban Allowlist plugin

Status: **GIANT HACK, USE AT YOUR OWN RISK**

Home Assistant has [a very useful IP banning feature](https://www.home-assistant.io/integrations/http/#ip-filtering-and-banning) which is nice for when you've got a private but externally facing instance that you'd like to reduce the odds on getting hacked.

However, it's got one little missing feature: IP allowlists. Without this, sometimes you get the problem that your home IP gets banned (because you've got something internal to your house using the external naming), which is a bit frustrating. The position of the core devs appears to be ["this is a bug with something else that we shouldn't workaround"](https://github.com/home-assistant/core/pull/52334), but meanwhile we're stuck with the banning happening every so often.

This integration (well, kinda) fixes this, but does so in the hackiest way possible, by reaching into the HTTP handler code and adding a wrapper around the banning code.

This does have a decent unit test suite, and is explicitly integration tested against every latest patch version of HA from 2023.8.4 up (i.e. for every `x.y.z` version, we test all values of `x.y` using the latest `z` value), but it's also doing something hacky enough that no guarantees are given. YMMV!

## Config

To use this, [install with HACS](https://hacs.xyz/) as [a custom repository](https://hacs.xyz/docs/faq/custom_repositories).

Then add to your `configuration.yaml` something like the following:
```
ban_allowlist:
  ip_addresses: ["my.ip.address", "another.ip.address"]
```
