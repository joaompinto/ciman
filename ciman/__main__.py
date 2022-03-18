import typer
from .cli import info, pull, tags, image, layer, main, history, run

app = typer.Typer()

app.callback()(main.main)

app.command()(history.history)
app.command()(info.info)
app.command()(pull.pull)
app.command(context_settings={"allow_extra_args": True})(run.run)
app.command()(tags.tags)
app.add_typer(image.app, name="image")
app.add_typer(layer.app, name="layer")


if __name__ == "__main__":
    app()
