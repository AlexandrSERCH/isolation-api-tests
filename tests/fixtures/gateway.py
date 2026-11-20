import pytest

from tests.clients.http.gateway.client import (
    GatewayHTTPTestClient,
    build_gateway_http_test_client,
)


@pytest.fixture
def gateway_http_test_client() -> GatewayHTTPTestClient:
    return build_gateway_http_test_client()
