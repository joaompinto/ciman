import typer
from ciman.registry import DockerRegistryClient
from ciman.view.info import print_tags_info


def tags(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    List all the tags available for an image
    """
    registry, repository, _ = DockerRegistryClient.parse_image_url(image_name)
    drc = DockerRegistryClient(registry)
    tags_info = drc.get_tags(repository)
    print_tags_info(tags_info)
