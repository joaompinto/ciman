from rich.console import Console
from rich.text import Text
from ..jsonrules import print_item
import json

console = Console()


def print_text(text):
    console.print(text)


def print_key(key, _):
    print_key_and_value(key, "")


def print_key_and_value(key, value):
    if isinstance(value, int):
        value = str(value)
    print_text(Text.assemble((f"{key[0] : <16}", "bold magenta"), value))


def print_checksum(key, value):
    sum_type, sum_val = value.split(":")
    print_text(
        Text.assemble(
            4 * " ", str(key[-2]), ": ", (sum_type, "bold white"), ":", sum_val
        )
    )


def delete_values(json_data, values_to_remove):
    if isinstance(json_data, dict):
        keys_to_delete = []
        for key in json_data.keys():
            value = json_data[key]
            if value in values_to_remove:
                keys_to_delete.append(key)
            else:
                delete_values(value, values_to_remove)
        for key in keys_to_delete:
            del json_data[key]
    if isinstance(json_data, list):
        for value in json_data:
            delete_values(value, values_to_remove)


def pretty_print(_, value):
    value = json.loads(value)
    delete_values(value, [False, "", None, {}])
    console.print_json(json.dumps(value), skip_keys=False)


json_print_rules = {
    1: print_key_and_value,
    "fsLayers": print_key,
    "history": print_key,
    "blobSum": print_checksum,
    "v1Compatibility": pretty_print,
}


def print_image_info(image_json):
    print_item(json_print_rules, [], image_json)