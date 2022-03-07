import typer
from .cli import info, pull, tags, image

app = typer.Typer()

app.command()(info.info)
app.command()(pull.pull)
app.command()(tags.tags)
app.add_typer(image.app, name="image")


def main():
    app()


if __name__ == "__main__":
    main()
