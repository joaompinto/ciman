import typer
import os
import stat
import subprocess
from ciman.cache.layers import LayersCache
from ciman.cache.images import ImagesCache
from print_err import print_err
from tempfile import TemporaryDirectory
from tarfile import TarFile
from pathlib import Path

LCACHE = LayersCache()
ICACHE = ImagesCache()


def run(
    ctx: typer.Context,
    image_name: str = typer.Argument(..., help="The name of the image"),
):
    """
    Show information for an image stored in a docker registry
    """
    proot_path = Path("~/.ciman", "bin", "proot").expanduser()
    if not proot_path.exists():
        print_err(f"Proot binary not found at {proot_path}", exit_code=1)

    if not os.access(proot_path, os.X_OK):
        os.chmod(proot_path, proot_path.stat().st_mode | stat.S_IEXEC)

    info = ICACHE.GetImage(image_name)
    if not info:
        print_err(f"No local image with name {image_name}", exit_code=2)
    with TemporaryDirectory() as tmp_dir_name:
        for layer in ICACHE.GetLayers(image_name):
            layer_name = layer["blobSum"]
            layer_fname = LCACHE.GetLayer(layer_name)
            with TarFile.open(layer_fname, "r:gz") as tar_file:
                tar_file.extractall(tmp_dir_name, numeric_owner=False)
        args = [proot_path, "-R", tmp_dir_name] + ctx.args
        subprocess.run(args, check=True, text=True)
