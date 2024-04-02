"""Integration test for ban allowlist."""

import shutil
import subprocess
import time
from pathlib import Path

import requests
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib3.exceptions import ProtocolError

env = Environment(loader=FileSystemLoader("config"), autoescape=select_autoescape())

config_folder = Path("config")
ban_ip_path = config_folder.joinpath("ip_bans.yaml")

root = Path(__file__).parent.parent
new_custom_components = config_folder.joinpath("custom_components", "ban_allowlist")
if new_custom_components.exists():
    shutil.rmtree(new_custom_components)

shutil.copytree(
    root.joinpath("custom_components", "ban_allowlist"), new_custom_components
)


def wait_for_http(port: int, host: str = "localhost", timeout: float = 5.0):
    """Wait for a particular HTTP host/port to start responding to GETs."""
    start_time = time.perf_counter()
    print(f"Waiting for http://{host}:{port}")
    while True:
        try:
            res = requests.get(f"http://{host}:{port}")
            res.raise_for_status()
            break
        except requests.exceptions.ConnectionError as ex:
            time.sleep(0.1)
            if not isinstance(ex.args[0], ProtocolError):
                print("Waiting", ex.args)
            if time.perf_counter() - start_time >= timeout:
                logs = subprocess.check_output(["docker-compose", "logs"])
                print("logs")
                print(logs)
                raise TimeoutError(
                    "Waited too long for the port {} on host {} to start accepting "
                    "connections.".format(port, host)
                ) from ex


def configure_ha(allowlist: list[str]) -> None:
    """Configure home-assistant with a particular allowlist."""
    configuration_template = env.get_template("configuration.yaml.j2")
    with config_folder.joinpath("configuration.yaml").open("w") as config_out:
        config_out.write(configuration_template.render(ALLOWLIST=allowlist))
    subprocess.check_call(["docker-compose", "down"])
    if ban_ip_path.exists():
        ban_ip_path.unlink()
    subprocess.check_call(["docker-compose", "up", "-d"])
    wait_for_http(8123)


def check_res(expected_results: list[int]):
    """
    Check that talking to HA gets a particular set of statuses.

    This is so we can check banning happens on later requests.
    """
    try:
        for index in range(len(expected_results)):
            res = requests.post(
                "http://localhost:8123/auth/login_flow/b4b20b5004a6baa2a1d903de46886ed2",
                json={"client_id": "http://localhost:8123/"},
            )
            assert res.ok is False, (res, res.text)
            assert res.status_code == expected_results[index], (res, res.text)
    finally:
        subprocess.check_call(["docker-compose", "down"])


configure_ha([])
check_res([404, 403])  # Second is after banning

ban_ip_file = ban_ip_path.open()
ban_ips: dict[str, object] = yaml.safe_load(ban_ip_file)
assert len(ban_ips) == 1, ban_ips
ban_ip = list(ban_ips.keys())[0]
print(f"Banned ip is {ban_ip}")

configure_ha([ban_ip])
check_res([404, 404])

assert not ban_ip_path.exists()
