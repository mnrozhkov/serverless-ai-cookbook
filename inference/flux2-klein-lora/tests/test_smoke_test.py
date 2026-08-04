import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "scripts" / "smoke-test.py"
SPEC = importlib.util.spec_from_file_location("flux2_klein_lora_smoke_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SMOKE_TEST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE_TEST)


def test_accepts_nebius_https_tunnel_fqdn():
    url = (
        "https://port8000-example.tunnel.applications.eu-north1.nebius.cloud/"
    )
    assert SMOKE_TEST.validate_base_url(url) == url.rstrip("/")


@pytest.mark.parametrize(
    ("url", "message"),
    [
        ("http://port8000-example.tunnel.applications.eu-north1.nebius.cloud", "HTTPS"),
        ("https://204.12.169.250:8000", "not an IP address"),
        ("https://[2001:db8::1]", "not an IP address"),
        ("https://localhost", "endpoint FQDN"),
        ("https://example.nebius.cloud/v1", "must not contain a path"),
    ],
)
def test_rejects_non_fqdn_or_non_https_base_urls(url, message):
    with pytest.raises(ValueError, match=message):
        SMOKE_TEST.validate_base_url(url)
