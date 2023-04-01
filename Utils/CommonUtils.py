
import json


def load_json(input_path:str):
    """
    :param input_path: input json file path
    :return: json data
    """
    with open(input_path, 'r') as jf:
        data = json.load(jf)
    return data