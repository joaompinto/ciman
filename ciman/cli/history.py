import typer
from ciman.registry import DockerRegistryClient, get_fqdn_image_name
from ciman.view.history import print_image_history


def history(image_name: str = typer.Argument(..., help="The name of the image"),):
    """
    Show information for an image stored in a docker registry
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    ri = drc.GetRepositoryInfo(image_name)
    print_image_history(ri)
