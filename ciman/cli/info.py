import typer
from ..registry import DockerRegistryClient, get_fqdn_image_name
from ..view.info import print_image_info


def info(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Show information for an image stored in a docker registry
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    ri = drc.GetRepositoryInfo(image_name)
    print_image_info(ri)
