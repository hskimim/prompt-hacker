from typing import List, Tuple, TypeVar
import numpy as np

T = TypeVar("T")


def split(arr: List[T], at: int) -> Tuple[List[T], List[T]]:
    if at < 0:
        raise ValueError("'at' should not be negative")
    return arr[:at], arr[at:]


def calc_jacaard_similarity_for_one_side(compare: str, criteria: str):
    return len(set(compare) & set(criteria)) / len(set(criteria))


def calc_cosine_sim(v1: List[float], v2: List[float]) -> float:
    # Convert the input vectors to numpy arrays
    vector1 = np.array(v1)
    vector2 = np.array(v2)

    if len(vector1) != len(vector2):
        raise ValueError("v1 and v2's dimension should be same")

    # Calculate dot product
    dot_product = np.dot(vector1, vector2)

    # Calculate the magnitude (Euclidean norm) of each vector
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)  # type: ignore
