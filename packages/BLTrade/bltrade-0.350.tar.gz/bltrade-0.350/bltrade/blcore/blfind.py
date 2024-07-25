# Python查找算法
# author:jiawenze
# date:2024-7-24

from typing import List,TypeVar,Generic

T = TypeVar('T')

def get_first(items: List[T]) -> T:
        """Return the first item in a list."""

        if items:
                return items[0]

def get_last(items:List[T]) -> T:
        """Return the last item in a list."""

        if items:
                return items[-1]


#test
"""
a=[81,2,3,4,15]
print(get_first([1,2,3,4,5]))
print(get_first(a))
print(get_last([1,2,3,4,5]))
print(get_last(a))
print(get_last([1]))
"""
