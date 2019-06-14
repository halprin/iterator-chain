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

    @staticmethod
    def _is_dict(something):
        return isinstance(something, dict)

    @staticmethod
    def _is_iterable(something):
        return not isinstance(something, str) and not isinstance(something, dict) and isinstance(something, collections.abc.Iterable)

    def _flatten(self, iterable, force_stop=False):
        for item in iterable:
            if force_stop:
                yield item
            elif self._is_dict(item):
                yield from self._flatten(item.items(), force_stop=True)
            elif self._is_iterable(item):
                yield from self._flatten(item)
            else:
                yield item

    def flatten(self):
        iterator = self._flatten(self._iterator)
        return _IntermediateIteratorChain(iterator)

    def sort(self, key=None, cmp=None, reverse=False):
        if key is None and cmp is not None:
            key = functools.cmp_to_key(cmp)
        iterator = iter(sorted(self._iterator, key=key, reverse=reverse))
        return _IntermediateIteratorChain(iterator)

    def reverse(self):
        forward = list(self._iterator)
        iterator = reversed(forward)
        return _IntermediateIteratorChain(iterator)

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
        except TypeError:
            total = default
        return total

    def reduce(self, function):
        return functools.reduce(function, self._iterator)

    def for_each(self, function):
        for item in self._iterator:
            function(item)

    def all_match(self, function):
        return all(map(function, self._iterator))

    def any_match(self, function):
        return any(map(function, self._iterator))

    def none_match(self, function):
        return not self.any_match(function)
