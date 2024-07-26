#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Unique Iteration Utilities.

* :any:`unique` - Unique Iterator
* :any:`uniquetuple` - Create tuple with unique elements
* :any:`uniquelist` - Create list with unique elements
"""


def uniquelist(iterable, key=None):
    """
    Return unique list.

    >>> uniquelist([1, 5, 2, 3, 3, 6, 7, 2, 3])
    [1, 5, 2, 3, 6, 7]

    The ``key`` callback allows to refine the duplicate detection:

    >>> uniquelist([(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'), (3, 'a')])
    [(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b')]
    >>> uniquelist([(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'), (3, 'a')], key=lambda item: item[1])
    [(5, 'a'), (2, 'b')]
    """
    return list(unique(iterable, key=key))


def uniquetuple(iterable, key=None):
    """
    Return unique tuple.

    >>> uniquetuple([1, 5, 2, 3, 3, 6, 7, 2, 3])
    (1, 5, 2, 3, 6, 7)

    The ``key`` callback allows to refine the duplicate detection:

    >>> uniquetuple([(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'), (3, 'a')])
    ((5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'))
    >>> uniquetuple([(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'), (3, 'a')], key=lambda item: item[1])
    ((5, 'a'), (2, 'b'))
    """
    return tuple(unique(iterable, key=key))


def unique(iterable, key=None):
    """
    Iterate over `iterable` and ensure that every item is just returned once.

    >>> iterator = unique([1, 3, 1, 3, 6, 3])
    >>> next(iterator)
    1
    >>> next(iterator)
    3
    >>> next(iterator)
    6
    >>> next(iterator)
    Traceback (most recent call last):
        ...
    StopIteration


    >>> iterator = unique([(5, 'a'), (2, 'b'), (3, 'a'), (4, 'b'), (3, 'a')], key=lambda item: item[1])
    >>> next(iterator)
    (5, 'a')
    >>> next(iterator)
    (2, 'b')
    >>> next(iterator)
    Traceback (most recent call last):
        ...
    StopIteration
    """
    seen = set()
    if key:
        for item in iterable:
            ident = key(item)
            if ident not in seen and not seen.add(ident):
                yield item
    else:
        for item in iterable:
            if item not in seen and not seen.add(item):
                yield item
