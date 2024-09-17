import re

def camel_to_snake(string):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', string).lower()

def convert_dict_keys_to_snake_case(d):
    if isinstance(d, list):
        return [convert_dict_keys_to_snake_case(i) if isinstance(i, (dict, list)) else i for i in d]
    return {camel_to_snake(k): convert_dict_keys_to_snake_case(v) if isinstance(v, (dict, list)) else v for k, v in d.items()}