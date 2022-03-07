import typer
from ..registry import DockerRegistryClient, get_fqdn_image_name
from ..view.info import print_tags_info


def tags(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    List all the tags available for an image
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    tags_info = drc.GetTags(image_name)
    print_tags_info(tags_info)
