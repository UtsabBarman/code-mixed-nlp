import json
import numpy as np
from json import JSONEncoder


class NumpyArrayEncoderForJSON(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def load_json(input_path: str):
    """
    :param input_path: input json file path
    :return: json data
    """
    with open(input_path, "r") as jf:
        data = json.load(jf)
    return data


def write_json(output_path: str, data: dict):
    """
    :param input_path: output json file path
    :param data: data dict
    :return: None
    """
    with open(output_path, "w") as jf:
        json.dump(data, jf, cls=NumpyArrayEncoderForJSON)


def normalize_token(x: str):
    """
    :param x: token to normalize
    :return: string
    """
    if x.startswith("@"):
        return "@_"
    elif x.startswith("#"):
        return "#_"
    else:
        return x.lower().strip()
