"""
Utilities for manipulating lists and sets
"""

from typing import List, Set, Iterable, Iterator, Tuple

# flatten list of lists
def flatten(l: List) -> List:
    return [item for sublist in l for item in sublist]

