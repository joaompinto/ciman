import httpx
import re
from rich import print as rprint

DEFAULT_REGISTRY = "https://index.docker.io"

API_URL = "/v2/"


class DockerRegistryClient(object):
    def __init__(
        self,
        registry=DEFAULT_REGISTRY,
        verify_ssl=None,
        api_version=None,
        username=None,
        password=None,
        auth_service_url="",
        api_timeout=None,
    ):
        self.api_url = f"{registry}{API_URL}"
        self.http_client = httpx.Client()
        self.auth_client = httpx.Client()

        request = self.http_client.get(self.api_url)
        if request.status_code == 401:
            auth_realm = request.headers.get("Www-Authenticate")
            if not auth_realm:
                request.raise_for_status()
            regex = re.compile('Bearer realm="(.*)",service="(.*)"')
            results = regex.findall(auth_realm)
            assert len(results) == 1
            self.auth_service, self.registry_service = results[0]

    def get_scoped_token(
        self, resource_type: str, resource_name: str, resource_actions: list
    ):

        url = (
            f"{self.auth_service}?scope={resource_type}:{resource_name}"
            + f":{','.join(resource_actions)}&service={self.registry_service}"
        )
        request = self.auth_client.get(url)
        request.raise_for_status()
        return request.json()["token"]

    def GetRepositoryInfo(self, name: str):
        if ":" in name:
            name, tag = name.split(":", 1)
        else:
            tag = "latest"
        if "/" not in name:
            name = f"library/{name}"
        token = self.get_scoped_token("repository", name, ["pull"])
        self.http_client.headers = {"Authorization": f"Bearer {token}"}
        manifest_url = f"{self.api_url}{name}/manifests/{tag}"
        request = self.http_client.get(manifest_url)
        request.raise_for_status()
        rprint(request.json())
