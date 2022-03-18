import json
import typer
from typing import Optional
from ciman.registry import DockerRegistryClient, get_fqdn_image_name
from ciman.view.info import print_image_info


def info(
    image_name: str = typer.Argument(..., help="The name of the image"),
    output_format: Optional[str] = typer.Option(
        None, "-o", "--output-format", help="Ouput format [json]"
    ),
):
    """
    Show information for an image stored in a docker registry
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    ri = drc.GetRepositoryInfo(image_name)
    if output_format == "json":
        print(json.dumps(drc.GetManifest(), indent=4))
    else:
        print_image_info(ri)
