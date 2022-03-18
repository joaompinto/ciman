import typer
from rich.table import Table
from ciman.view.console import console
from ciman.cache.images import ImagesCache
from ciman.view.info import sizeof_fmt
from ciman.view.info import print_image_info
from ciman.view.info import print_key_and_value
from print_err import print_err


ICACHE = ImagesCache()

app = typer.Typer()


@app.command()
def ls():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Local Name")
    table.add_column("Size", justify="right")
    table.add_column("Source")

    for image_name in ICACHE.ListImages():
        image_info = ICACHE.GetImage(image_name)
        image_size = ICACHE.GetImageSize(image_name)
        table.add_row(image_name, sizeof_fmt(image_size), image_info["source"])
    console.print(table)


@app.command()
def inspect(image_name: str = typer.Argument(..., help="The name of the image")):
    info = ICACHE.GetImage(image_name)
    if not info:
        print_err(f"No local image with name {image_name}", exit_code=2)
    print_key_and_value(["Source"], info["source"])
    print_image_info(info["manifest"])
