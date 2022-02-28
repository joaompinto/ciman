def print_item(json_rules, key, value):

    # print("KVL", key, value, type(value))
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


def check_name_rules(json_rules, key, value):
    """Check key name rules"""
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
