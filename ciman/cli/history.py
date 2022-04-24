import typer
from ciman.registry import DockerRegistryClient
from ciman.view.history import print_image_history


def history(image_name: str = typer.Argument(..., help="The name of the image"),):
    """
    Show information for an image stored in a docker registry
    """
    registry, repository, tag = DockerRegistryClient.parse_image_url(image_name)
    drc = DockerRegistryClient(registry)
    manifest = drc.get_manifest(repository, tag)
    print_image_history(manifest)
