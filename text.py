from typing import Any, List, Tuple

def find_sequence(a: List[Any], seq: List[Any], start: int = 0, end: int = -1) -> Tuple[int] | None:
    """
    Find the first occurrence of a sequence within a list.

    Args:
        a (List[Any]): The list to search within.
        seq (List[Any]): The sequence to find.
        start (int, optional): The starting index for the search. Defaults to 0.
        end (int, optional): The ending index for the search. Defaults to -1.

    Returns:
        Tuple[int] | None: The index of the first occurrence of the sequence, or None if not found.
    """
    if not (a and seq): return None
    try:
        print(a)
        print(seq)
        first = seq[0]
        i = a[start:end].index(first)
        print(i)
    except ValueError:
        print("none")
        return None

    if a[i:i+len(seq)] == seq:
        return i

def find_elements_after_sequence(a: List[Any], seq: List[Any], lookahead: int = 1) -> List[Any]:
    """
    Finds elements in list `a` that occur immediately after the sequence `seq`.

    Args:
        a (List[Any]): The list to search for elements.
        seq (List[Any]): The sequence to look for in `a`.

    Returns:
        List[Any]: A list of elements that occur immediately after `seq` in `a`.
    """
    if not a: return []
    if not seq: return a

    words = []
    current_index = 0
    while current_index := find_sequence(a, seq, start=current_index):
        words.append(a[current_index+len(seq):current_index+len(seq)+lookahead])

def test_find_sequence():
    # Test case 1: Sequence is found in the middle of the list
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = [4, 5, 6]
    assert find_sequence(a, seq) == 3

    # Test case 2: Sequence is found at the beginning of the list
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = [1, 2, 3]
    assert find_sequence(a, seq) == 0

    # Test case 3: Sequence is found at the end of the list
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = [6, 7]
    assert find_sequence(a, seq) == 5

    # Test case 4: Sequence is not found in the list
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = [8, 9, 10]
    assert find_sequence(a, seq) is None

    # Test case 5: Empty list
    a = []
    seq = [1, 2, 3]
    assert find_sequence(a, seq) is None

    # Test case 6: Empty sequence
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = []
    assert find_sequence(a, seq) == 0

    # Test case 7: Start and end indices specified
    a = [1, 2, 3, 4, 5, 6, 7]
    seq = [3, 4, 5]
    assert find_sequence(a, seq, start=1, end=6) == 1

    print("All test cases pass")

test_find_sequence()