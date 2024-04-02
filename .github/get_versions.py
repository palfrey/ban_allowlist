"""Get all the Home assistant versions that we want to run integration tests against."""

import json
import re

import requests
from awesomeversion import AwesomeVersion

data = requests.get("https://pypi.org/simple/homeassistant/")
data.raise_for_status()

min_supported = AwesomeVersion("2023.8.4")

raw = data.text
version_pattern = re.compile("homeassistant-([^#-]+).tar.gz")
versions = [AwesomeVersion(v) for v in version_pattern.findall(raw)]
versions = [v for v in versions if v.simple and v >= min_supported]
latest_minors = []
for version in versions:
    for latest_minor in list(latest_minors):
        if version == latest_minor:
            break
        diff = latest_minor.diff(version)
        if diff.major is False and diff.minor is False:
            if latest_minor > version:
                break
            latest_minors.remove(latest_minor)
    else:
        latest_minors.append(version)
output_versions = [latest_minor.string for latest_minor in latest_minors]
print(f"versions={json.dumps(output_versions)}")
