import json
from ciman.view.console import console


def print_layer_info(layer_json: dict):
    container_config = layer_json["container_config"]
    cmd = container_config["Cmd"]
    full_cmd = " ".join(cmd)

    if len(cmd) == 1:
        cmd = cmd[0]

    if full_cmd.startswith("/bin/sh -c #(nop) "):
        cmd = full_cmd[18:]

    if isinstance(cmd, str):
        cmd = cmd.replace("\t", "").strip()
    print(str(cmd))
    console.print("---", style="bold green")


def print_image_history(image_json: dict):
    def find_child(layers: list, current_layer: dict):
        for item in layers:
            if item.get("parent") == current_layer["id"]:
                return item

    history = image_json["history"]
    for i, item in enumerate(history):
        history[i] = json.loads(item["v1Compatibility"])

    top_layer = [i for i in history if not i.get("parent")]
    assert len(top_layer) == 1
    current_layer = top_layer[0]
    while current_layer:
        print_layer_info(current_layer)
        current_layer = find_child(history, current_layer)
