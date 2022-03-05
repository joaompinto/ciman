import typer
from .registry import DockerRegistryClient, get_fqdn_image_name
from .view.info import print_image_info, sizeof_fmt
from .view.info import print_tags_info

app = typer.Typer()


@app.command()
def info(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Show information for an image stored in a docker registry
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    ri = drc.GetRepositoryInfo(image_name)
    print_image_info(ri)


@app.command()
def pull(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Pull image from a docker registry
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    drc.GetRepositoryInfo(image_name)
    print("Layers")
    for i, layer in enumerate(drc.GetLayers()):
        layer_info = drc.GetLayerInfo(layer)
        layer_size = int(layer_info["content-length"])
        print(i, layer["blobSum"], layer_size, sizeof_fmt(layer_size))
        #  print(layer)
    #  img_puller = ImagePuller(ri)
    #  img_puller.pull()


@app.command()
def tags(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    List all the tags available for an image
    """
    registry, image_name = get_fqdn_image_name(image_name)
    drc = DockerRegistryClient(registry)
    tags_info = drc.GetTags(image_name)
    print_tags_info(tags_info)


def main():
    app()


if __name__ == "__main__":
    main()
