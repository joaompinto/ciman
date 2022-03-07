import typer

from ..images_cache import ImagesCache
from ..view.info import sizeof_fmt

ICACHE = ImagesCache()

app = typer.Typer()


@app.command()
def ls():
    for image_name in ICACHE.ListImages():

        image_info = ICACHE.GetImage(image_name)
        image_size = ICACHE.GetImageSize(image_name)
        print(image_name, image_info["source"], sizeof_fmt(image_size), image_size)
