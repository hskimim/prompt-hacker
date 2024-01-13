import numpy as np


def calc_jacaard_similarity_for_one_side(compare: str, criteria: str):
    return len(set(compare) & set(criteria)) / len(set(criteria))


def calc_cosine_sim(v1: list[list[float]], v2: list[list[float]]) -> list[float]:
    if len(v1[0]) != len(v2[0]):
        raise ValueError("v1 and v2's dimension should be same")
    unit_v1 = np.array(v1) / np.linalg.norm(v1, axis=1)
    unit_v2 = np.array(v2) / np.linalg.norm(v2, axis=1)

    return np.dot(unit_v1, unit_v2.T).reshape(-1)
