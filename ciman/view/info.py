from rich.console import Console
from rich.text import Text

console = Console()


def print_key(key, value):
    print_key_and_value(key, "")


def print_key_and_value(key, value):
    text = Text.assemble((f"{key[0] : <16}", "bold magenta"), str(value))
    console.print(text)


def print_checksum(key, value):
    sum_type, sum_val = value.split(":")
    text = Text.assemble(
        16 * " ", str(key[-2]), ": ", (sum_type, "bold white"), ":", sum_val
    )
    console.print(text)


def pretty_print(key, value):
    # text = Text.assemble((f'{key[0] : <16}', "bold magenta"), str(key))
    # console.print(text)
    console.print_json(value)


json_print_rules = {
    1: print_key_and_value,
    "fsLayers": print_key,
    "history": print_key,
    "blobSum": print_checksum,
    "v1Compatibility": pretty_print,
}


def check_name_rules(json_rules, key, value):
    """ Check key name rules """
    for rule_key, rule_func in json_rules.items():
        if isinstance(rule_key, str) and rule_key.count(".") == 0:
            if key and key[-1] == rule_key:
                # print("MATCH", rule_key)
                rule_func(key, value)


def check_level_rules(json_rules, key, value):
    level = len(key)
    # Check rule levels only for leafs
    for rule_key, rule_func in json_rules.items():
        if isinstance(rule_key, int):
            if level == rule_key:
                rule_func(key, value)


def print_item(json_rules, key, value):

    # print("KVL", key, value, level)
    check_name_rules(json_rules, key, value)

    if isinstance(value, list):
        for i, v in enumerate(value):
            print_item(json_rules, key + [i], v)
        return

    if isinstance(value, dict):
        for k, v in value.items():
            print_item(json_rules, key + [k], v)
        return

    check_level_rules(json_rules, key, value)


def print_image_info(image_json):
    print_item(json_print_rules, [], image_json)
