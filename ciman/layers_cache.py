from pathlib import Path
import os
import shutil


CIMAN_BASE_DIR = os.getenv("CIMAN_BASE", "~/.ciman/layers")
CACHE_DIR = Path(CIMAN_BASE_DIR).expanduser()


class LayersCache:
    def GetLayer(self, layer_name):
        layer_fname = Path(CACHE_DIR, f"{layer_name}.tar.gz")
        if layer_fname.exists():
            return layer_fname

    def StoreLayer(self, layer_name, layer_fname):
        if not CACHE_DIR.exists():
            os.makedirs(CACHE_DIR)
        cached_layer_fname_tmp = Path(CACHE_DIR, f"{layer_name}.tmp")
        cached_layer_fname = Path(CACHE_DIR, f"{layer_name}.tar.gz")
        shutil.copy(layer_fname, cached_layer_fname_tmp)
        os.rename(cached_layer_fname_tmp, cached_layer_fname)
