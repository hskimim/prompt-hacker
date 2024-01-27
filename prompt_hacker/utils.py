import json
import os
from typing import Any

import numpy as np


def calc_jacaard_similarity_for_one_side(compare: str, criteria: str):
    return len(set(compare) & set(criteria)) / len(set(criteria))


def calc_cosine_sim(v1: list[list[float]], v2: list[list[float]]) -> list[float]:
    if len(v1[0]) != len(v2[0]):
        raise ValueError("v1 and v2's dimension should be same")
    unit_v1 = np.array(v1) / np.linalg.norm(v1, axis=1)
    unit_v2 = np.array(v2) / np.linalg.norm(v2, axis=1)

    return np.dot(unit_v1, unit_v2.T).reshape(-1)


def read_json(fname: str) -> list[dict[str, str]]:
    with open(fname, "r") as f:
        doc = f.read()
    return json.loads(doc)


def read_file_with_rel_path(relative_file_path: str) -> Any:
    module_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(module_directory, relative_file_path))
    return read_json(file_path)
