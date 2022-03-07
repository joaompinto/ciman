from pathlib import Path
import os
import json
from .layers_cache import LayersCache

CIMAN_BASE_DIR = os.getenv("CIMAN_BASE", "~/.ciman/images")
CACHE_DIR = Path(CIMAN_BASE_DIR).expanduser()

ICACHE = LayersCache()


class ImagesCache:
    def ListImages(self):
        image_list = []
        for image_path in Path(CACHE_DIR).glob("*.json"):
            image_list.append(image_path.stem)
        return image_list

    def GetImage(self, image_name):
        layer_fname = Path(CACHE_DIR, f"{image_name}.json")
        if layer_fname.exists():
            with open(layer_fname) as json_file:
                return json.load(json_file)

    def GetImageSize(self, image_name):
        img_info = self.GetImage(image_name)
        layers = img_info["manifest"]["fsLayers"]
        total = sum(layer["size"] for layer in layers)
        return total

    def StoreImage(self, local_image_name, image_json):
        if not CACHE_DIR.exists():
            os.makedirs(CACHE_DIR)
        cached_fname_tmp = Path(CACHE_DIR, f"{local_image_name}.tmp")
        with open(cached_fname_tmp, "wt+") as cached_tmp:
            json.dump(image_json, cached_tmp)
        cached_fname = Path(CACHE_DIR, f"{local_image_name}.json")
        os.rename(cached_fname_tmp, cached_fname)
