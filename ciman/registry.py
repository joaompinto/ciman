import httpx
import re
import os

DEFAULT_REGISTRY = os.environ.get("DOCKER_REGISTRY", "registry-1.docker.io")

API_URL = "/v2/"


class DockerRegistryClient(object):
    def __init__(
        self,
        registry,
        verify_ssl=None,
        api_version=None,
        username=None,
        password=None,
        auth_service_url="",
        api_timeout=None,
    ):
        if "://" not in registry:
            registry = f"https://{registry}"
        self.api_url = f"{registry}{API_URL}"
        self.http_client = httpx.Client()
        self.auth_client = httpx.Client()
        self.requires_authentication = False
        self.repository_info = {}
        self.last_reference = None
        self.last_name = None

        request = self.http_client.get(self.api_url)
        if request.status_code == 401:
            self.requires_authentication = True
            auth_realm = request.headers.get("Www-Authenticate")
            if not auth_realm:
                request.raise_for_status()
            regex = re.compile('Bearer realm="(.*)",service="(.*)"')
            results = regex.findall(auth_realm)
            assert len(results) == 1
            self.auth_service, self.registry_service = results[0]
        else:
            request.raise_for_status()

    def get_scoped_token(
        self, resource_type: str, resource_name: str, resource_actions: list
    ):
        if not self.requires_authentication:
            return
        url = (
            f"{self.auth_service}?scope={resource_type}:{resource_name}"
            + f":{','.join(resource_actions)}&service={self.registry_service}"
        )
        request = self.auth_client.get(url)
        request.raise_for_status()
        token = request.json()["token"]
        self.http_client.headers = {"Authorization": f"Bearer {token}"}

    def GetRepositoryInfo(self, name: str):
        if ":" in name:
            name, tag = name.split(":", 1)
        else:
            tag = "latest"
        if "/" not in name:
            name = f"library/{name}"
        self.last_name = name
        reference = f"{name}:{tag}"
        self.last_reference = reference
        self.get_scoped_token("repository", name, ["pull"])
        manifest_url = f"{self.api_url}{name}/manifests/{tag}"
        request = self.http_client.get(manifest_url)
        request.raise_for_status()
        self.repository_info[reference] = request.json()
        self.FillLayerSize()
        return self.repository_info[reference]

    def GetTags(self, name):
        if "/" not in name:
            name = f"library/{name}"
        self.get_scoped_token("repository", name, ["pull"])
        tags_url = f"{self.api_url}{name}/tags/list"
        request = self.http_client.get(tags_url)
        request.raise_for_status()
        return request.json()

    def GetCatalog(self):
        url = f"{self.api_url}_catalog"
        request = self.http_client.get(url)
        request.raise_for_status()

    def GetLayers(self):
        return self.repository_info[self.last_reference]["fsLayers"]

    def GetLayerInfo(self, layer):
        url = f"{self.api_url}{self.last_name}/blobs/{layer['blobSum']}"
        request = self.http_client.head(url, follow_redirects=True)
        request.raise_for_status()
        return request.headers

    def FillLayerSize(self):
        layers = self.repository_info[self.last_reference]["fsLayers"]
        for layer in layers:
            layer_info = self.GetLayerInfo(layer)
            layer["size"] = int(layer_info["content-length"])


def get_fqdn_image_name(image_name: str):
    registry = DEFAULT_REGISTRY
    protocol_prefix = "https://"
    protocol_mark = image_name.find("://")
    if protocol_mark > -1:
        protocol_prefix = image_name[: protocol_mark + 3]
        image_name = image_name[protocol_mark + 3 :]
    if "/" in image_name:
        first_part, other_parts = image_name.split("/", 1)
        if "." in first_part:
            image_name = other_parts
            registry = f"{protocol_prefix}{first_part}"
    return registry, image_name
