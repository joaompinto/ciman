from pytest_httpserver import HTTPServer
from ciman.view.registry.registry import DockerRegistryClient


def test_json_client(httpserver: HTTPServer):

    headers = {
        "Www-Authenticate": f'Bearer realm="{httpserver.url_for("/token/")}",service="registry.docker.io"'
    }
    unauthorized_json = {
        "errors": [
            {
                "code": "UNAUTHORIZED",
                "message": "authentication required",
                "detail": None,
            }
        ]
    }
    httpserver.expect_request("/v2/").respond_with_json(
        unauthorized_json, status=401, headers=headers
    )

    _ = DockerRegistryClient(httpserver.url_for(""))
