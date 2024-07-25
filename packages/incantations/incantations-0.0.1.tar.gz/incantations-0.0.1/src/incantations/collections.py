from typing import Iterable, TypeVar, List, Generator
from itertools import islice

T = TypeVar('T')

def unique(iterable: Iterable[T]) -> List[T]:
    """
    Remove duplicate elements from an iterable while preserving order.
    
    Args:
        iterable (Iterable[T]): The input iterable.
    
    Returns:
        List[T]: A list of unique elements in the order they first appeared.
    
    Example:
        >>> unique([1, 2, 2, 3, 1, 4])
        [1, 2, 3, 4]
    """
    seen = set()
    return [x for x in iterable if not (x in seen or seen.add(x))]

def chunkify(iterable: Iterable[T], chunk_size: int) -> Generator[List[T], None, None]:
    """
    Yield successive chunks from the iterable of the specified size.
    
    Args:
        iterable (Iterable[T]): The input iterable to be chunked.
        chunk_size (int): The size of each chunk.
    
    Yields:
        List[T]: A chunk of the iterable with the specified size.
    
    Example:
        >>> list(chunkify(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    iterator = iter(iterable)
    return iter(lambda: list(islice(iterator, chunk_size)), [])

