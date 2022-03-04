import typer
from .registry import DockerRegistryClient
from .view.info import print_image_info
from .view.info import print_tags_info

app = typer.Typer()


@app.command()
def info(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Show information for an image stored in a docker registry
    """
    drc = DockerRegistryClient()
    ri = drc.GetRepositoryInfo(image_name)
    print_image_info(ri)


@app.command()
def pull(name: str = typer.Argument(..., help="The name of the user to greet")):
    """
    Pull image from a docker registry into a local directory
    """
    typer.echo("Not implemented yet")


@app.command()
def tags(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    List all the tags available for an image
    """
    drc = DockerRegistryClient()
    tags_info = drc.GetTags(image_name)
    print_tags_info(tags_info)


def main():
    app()


if __name__ == "__main__":
    main()
