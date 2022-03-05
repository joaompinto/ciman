class ImagePuller:
    def __init__(self, image_info: dict):
        self.image_info = image_info

    def pull(self):
        for layer in self.image_info["fsLayers"]:
            print(layer)
