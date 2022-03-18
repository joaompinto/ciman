import typer
from rich.table import Table
from ciman.view.console import console
from ciman.cache.layers import LayersCache
from ciman.view.info import sizeof_fmt

app = typer.Typer()

LCACHE = LayersCache()


@app.command()
def ls():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Hash")
    table.add_column("Size", justify="right")

    for layer_name in LCACHE.GetItems():
        size = LCACHE.GetSize(layer_name)
        table.add_row(layer_name, sizeof_fmt(size))
    console.print(table)
