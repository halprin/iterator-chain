import itertools


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
        pass

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
        pass

    def first(self, default=None):
        return next(itertools.islice(self._iterator, 1), default)

    def last(self, default=None):
        pass

    def max(self):
        pass

    def min(self):
        pass

    def sum(self):
        pass

    def reduce(self, function):
        pass

    def for_each(self, function):
        pass

    def all_match(self, function):
        pass

    def any_match(self, function):
        pass

    def none_match(self, function):
        pass
