import itertools
import functools
import collections


class _IntermediateIteratorChain:
    def __init__(self, iterator):
        self._iterator = iterator

    # Chain methods
    def map(self, function):
        iterator = map(function, self._iterator)
        return _IntermediateIteratorChain(iterator)

    def skip(self, number):
        iterator = itertools.islice(self._iterator, number, None)
        return _IntermediateIteratorChain(iterator)

    def filter(self, function):
        iterator = filter(function, self._iterator)
        return _IntermediateIteratorChain(iterator)

    def distinct(self):
        iterator = self._distinct()
        return _IntermediateIteratorChain(iterator)

    def _distinct(self):
        seen = set()
        for item in itertools.filterfalse(seen.__contains__, self._iterator):
            seen.add(item)
            yield item

    def limit(self, max_size):
        iterator = itertools.islice(self._iterator, max_size)
        return _IntermediateIteratorChain(iterator)

    def flatten(self):
        pass

    def sort(self):
        pass

    def reverse(self):
        pass

    # Termination methods
    def list(self):
        return list(self._iterator)

    def count(self):
        return sum(1 for _ in self._iterator)

    def first(self, default=None):
        return next(itertools.islice(self._iterator, 1), default)

    def last(self, default=None):
        try:
            end = collections.deque(self._iterator, maxlen=1).pop()
        except IndexError:
            end = default
        return end

    def max(self, default=None):
        return max(self._iterator, default=default)

    def min(self, default=None):
        return min(self._iterator, default=default)

    def sum(self, default=None):
        try:
            total = sum(self._iterator)
        except TypeError as error:
            if default is None:
                raise error
            else:
                total = default
        return total

    def reduce(self, function):
        return functools.reduce(function, self._iterator)

    def for_each(self, function):
        pass

    def all_match(self, function):
        for item in self._iterator:
            item_matches = function(item)
            if not item_matches:
                return False
        return True

    def any_match(self, function):
        for item in self._iterator:
            item_matches = function(item)
            if item_matches:
                return True
        return False

    def none_match(self, function):
        return not self.any_match(function)
