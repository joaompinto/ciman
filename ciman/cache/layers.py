from pathlib import Path
import os
import shutil


CIMAN_BASE_DIR = os.getenv("CIMAN_BASE", "~/.ciman/layers")
CACHE_DIR = Path(CIMAN_BASE_DIR).expanduser()


class LayersCache:
    def GetItems(self):
        item_list = []
        for layer_path in Path(CACHE_DIR).glob("*.tgz"):
            item_list.append(layer_path.stem)
        return item_list

    def GetLayer(self, layer_name):
        layer_fname = Path(CACHE_DIR, f"{layer_name}.tgz")
        if layer_fname.exists():
            return layer_fname

    def GetSize(self, layer_name):
        layer_fname = Path(CACHE_DIR, f"{layer_name}.tgz")
        return layer_fname.stat().st_size

    def StoreLayer(self, layer_name, layer_fname):
        os.makedirs(CACHE_DIR, exist_ok=True)
        cached_layer_fname_tmp = Path(CACHE_DIR, f"{layer_name}.tmp")
        cached_layer_fname = Path(CACHE_DIR, f"{layer_name}.tgz")
        shutil.copy(layer_fname, cached_layer_fname_tmp)
        os.rename(cached_layer_fname_tmp, cached_layer_fname)
