import typer
from .registry import DockerRegistryClient

app = typer.Typer()


@app.command()
def info(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Show information for an image stored in a docker registry
    """
    drc = DockerRegistryClient()
    drc.GetRepositoryInfo(image_name)


@app.command()
def pull(name: str = typer.Argument(..., help="The name of the user to greet")):
    """
    Pull image from a docker registry into a local directory
    """
    typer.echo("Not implemented yet")


def main():
    app()


if __name__ == "__main__":
    main()
