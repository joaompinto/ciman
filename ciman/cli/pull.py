from tempfile import NamedTemporaryFile
from functools import partial
from queue import Queue
import typer
from rich.progress import Progress
import threading
from rich.progress import (
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    BarColumn,
)
from ciman.registry import DockerRegistryClient
from ciman.cache.layers import LayersCache
from ciman.cache.images import ImagesCache
from ciman.view.info import sizeof_fmt

LCACHE = LayersCache()
ICACHE = ImagesCache()


def unique_layers(layers):
    """return layers with unique blobSum"""
    seen_sums = []
    un_layers = []
    for layer in layers:
        blobSum = layer["blobSum"]
        if blobSum in seen_sums:
            continue
        seen_sums.append(blobSum)
        un_layers.append(layer)
    return un_layers


def only_not_cached(layers):
    """return layers which are not cached"""
    not_cached = []
    for layer in layers:
        digest = layer["digest"]
        if LCACHE.GetLayer(digest):
            print(f"Layer {digest} found cached")
        else:
            not_cached.append(layer)
    return not_cached


def pull(image_name: str = typer.Argument(..., help="The name of the image")):
    """
    Pull image from a docker registry
    """
    registry, repository, tag = DockerRegistryClient.parse_image_url(image_name)
    drc = DockerRegistryClient(registry)
    manifest = drc.get_manifest(repository, tag)
    source_reference = f"{registry}/{repository}:{tag}"
    layers = manifest["layers"]
    layers = only_not_cached(layers)
    local_image_name = f"{repository}:{tag}"
    total_size = sum([layer["size"] for layer in layers])
    print(
        f"Pulling {len(layers)} layer(s) [{sizeof_fmt(total_size)}] "
        f"for image {source_reference} to local image {local_image_name}"
    )
    if len(layers) == 0:
        print("All layers found on cache")
    else:
        pull_layers_in_threads(drc, layers)

    image_json = {"source": source_reference, "manifest": manifest}

    ICACHE.StoreImage(local_image_name, image_json)


def pull_layers_in_threads(drc, layers):
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TransferSpeedColumn(),
        DownloadColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    ) as progress:
        result_queue = Queue()
        for layer in layers:
            total = layer["size"]
            task = progress.add_task(f'Downloading...{layer["blobSum"]}', total=total)
            download_thread = threading.Thread(
                target=download_layer, args=(drc, layer, task, result_queue)
            )
            download_thread.start()
        running_threads = len(layers)
        while running_threads:
            task, delta = result_queue.get()
            if delta is None:
                running_threads -= 1
            progress.update(task, advance=delta)


def download_layer(drc, layer, task, result_queue):
    def update_progress(task, result_queue, item):
        result_queue.put((task, item))

    try:
        with NamedTemporaryFile() as tmp_fname:
            drc.GetLayer(layer, partial(update_progress, task, result_queue), tmp_fname)
            LCACHE.StoreLayer(layer["blobSum"], tmp_fname.name)
    except:  # noqa: E722
        result_queue.put((task, None))
        raise

    result_queue.put((task, None))
