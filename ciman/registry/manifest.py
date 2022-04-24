from . import specs


class DockerManifest:
    def __init__(self, docker_registry, manifest_json: dict, expand_config: bool):
        assert manifest_json["schemaVersion"] == 2  # Support only v2 Schemas
        assert manifest_json["mediaType"] == specs.Manifests.DOCKER_DIST_V2
