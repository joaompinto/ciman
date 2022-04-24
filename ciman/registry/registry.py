import httpx
from httpx import Timeout
import re
import os
from .manifest import DockerManifest
from . import specs

DEFAULT_REGISTRY = os.environ.get("DOCKER_REGISTRY", "registry-1.docker.io")
API_URL = "/v2/"


class DockerRegistryClient(object):
    def __init__(
        self, registry, verify=True, username=None, password=None, timeout=5.0
    ):
        self.api_url = self.fq_api_url(registry)  # Prefer full qualified url
        self.http_client = httpx.Client(verify=verify, timeout=Timeout(timeout=timeout))
        self.auth_client = None
        self.repository_info = {}
        self.last_reference = None
        self.last_name = None
        self.authenticate()

    @staticmethod
    def parse_image_url(url: str) -> tuple:
        tag = "latest"
        url = url.strip("/")
        parts = url.split("/")
        if ":" in parts[-1]:
            image, tag = parts[-1].split()
            parts[-1] = image
        if "." in parts[0]:
            registry = parts[0]
            repository = "/".join(parts[1:])
        else:
            registry = DEFAULT_REGISTRY
            repository = "/".join(parts)
        if "/" not in repository:
            repository = f"library/{repository}"
        return registry, repository, tag

    @staticmethod
    def fq_api_url(registry) -> str:
        """Return the full qualified url for a registry"""
        registry = registry.strip("/")
        if "://" not in registry:
            registry = f"https://{registry}"
        return f"{registry}{API_URL}"

    @staticmethod
    def fq_image_name(name: str) -> tuple:
        """Return the full qualified name and tag"""
        if ":" in name:
            name, tag = name.split(":", 1)
        else:
            tag = "latest"
        if "/" not in name:
            name = f"library/{name}"
        return name, tag

    def authenticate(self):
        """perform Docker Registry v2 token authentication"""
        #   https://docs.docker.com/registry/spec/auth/token/
        request = self.http_client.get(self.api_url)
        if request.status_code == 401:
            self.auth_client = httpx.Client()
            auth_realm = request.headers.get("Www-Authenticate")
            if not auth_realm:
                request.raise_for_status()
            regex = re.compile('Bearer realm="(.*)",service="(.*)"')
            results = regex.findall(auth_realm)
            assert len(results) == 1
            self.auth_service, self.registry_service = results[0]
        else:
            request.raise_for_status()

    def _set_auth_token(self, token):
        self.http_client.headers["Authorization"] = f"Bearer {token}"

    def _auth_get(self, url):
        request = self.auth_client.get(url)
        request.raise_for_status()
        return request.json()

    def _http_get(self, url, follow_redirects=False):
        request = self.http_client.get(url, follow_redirects=follow_redirects)
        request.raise_for_status()
        return request.json()

    def _set_scoped_token(
        self, resource_type: str, resource_name: str, resource_actions: list
    ):
        if not self.auth_client:  # Registry does not require authentication
            return

        url = (
            f"{self.auth_service}?scope={resource_type}:{resource_name}"
            + f":{','.join(resource_actions)}&service={self.registry_service}"
        )

        token = self._auth_get(url)["token"]
        self._set_auth_token(token)

    def expand_config(self, manifest):
        """Replace the config key with it's blob content"""
        config = manifest["config"]
        manifest["config"] = self.get_blob(config["digest"])

    def get_manifest(
        self, name: str, tag, expand_config: bool = True
    ) -> DockerManifest:
        self.last_name = name
        # reference = f"{name}:{tag}"
        # self.last_reference = reference
        self._set_scoped_token("repository", name, ["pull"])
        self.http_client.headers["Accept"] = specs.Manifests.DOCKER_DIST_V2
        manifest_url = f"{self.api_url}{name}/manifests/{tag}"
        reply = self._http_get(manifest_url)
        if "config" in reply and expand_config:
            self.expand_config(reply)
        return reply

    def get_tags(self, name):
        if "/" not in name:
            name = f"library/{name}"
        self.get_scoped_token("repository", name, ["pull"])
        tags_url = f"{self.api_url}{name}/tags/list"
        return self._http_get(tags_url)

    def get_catalog(self):
        url = f"{self.api_url}_catalog"
        return self._http_get(url)

    def get_blob(self, blob_sum, update_hook=None, output_filename=None):
        url = f"{self.api_url}{self.last_name}/blobs/{blob_sum}"
        if output_filename:
            with httpx.stream(
                "GET", url, follow_redirects=True, headers=self.http_client.headers
            ) as r:
                r.raise_for_status()
                with open(output_filename, "wb+") as output_file:
                    for data in r.iter_bytes(chunk_size=50000):
                        output_file.write(data)
                        if update_hook:
                            update_hook(len(data))
        else:
            return self._http_get(url, follow_redirects=True)


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
