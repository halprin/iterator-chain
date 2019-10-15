import itertools
import functools
import collections


class _IntermediateIteratorChain:
    def __init__(self, iterator):
        self._iterator = iterator

    # Chain methods
    def map(self, function):
        """
        Will run the `function` across all the elements in the iterator.

        :param function: A function that takes a single argument.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = map(function, self._iterator)
        return _IntermediateIteratorChain(iterator)

    def filter(self, function):
        """
        Will run the `function` on every element.  `function` should return a truthy or falsy value.  On true, the element will stay; on false, the element will be removed.

        :param function: A function that takes a single argument.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = filter(function, self._iterator)
        return _IntermediateIteratorChain(iterator)

    def skip(self, number):
        """
        The `number` number of elements will be skipped over and effectively removed.

        :param number: An integer.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._skip(number)
        return _IntermediateIteratorChain(iterator)

    def _skip(self, number):
        return itertools.islice(self._iterator, number, None)

    def distinct(self):
        """
        Any duplicates will be removed.

        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._distinct()
        return _IntermediateIteratorChain(iterator)

    def _distinct(self):
        seen = set()
        for item in itertools.filterfalse(seen.__contains__, self._iterator):
            seen.add(item)
            yield item

    def limit(self, max_size):
        """
        The iterator will stop after `max_size` elements.  Any elements afterward are effectively removed.

        :param max_size: An integer.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._limit(max_size)
        return _IntermediateIteratorChain(iterator)

    def _limit(self, max_size):
        return itertools.islice(self._iterator, max_size)

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
        """
        Any element that is an iterable itself will have its elements iterated over first before continuing with the remaining elements.  Strings (`str`) do not count as an iterable for this method.  Dictionaries flatten to its item tuples.

        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._flatten(self._iterator)
        return _IntermediateIteratorChain(iterator)

    def sort(self, key=None, cmp=None, reverse=False):
        """
        Sorts the iterator based on the elements' values.  Use `key` or `cmp` to make a custom comparison.  If `key` is specified, `cmp` cannot be used.  This method is expensive because it must serialize all the values into a sequence.

        :param key: Keyword.  A function of one argument that is used to extract a comparison key from each element.
        :param cmp: Keyword.  A Python 2.x "cmp" function that takes two arguments.
        :param reverse: Keyword.  If set to `True`, the elements will be sorted in the reverse order.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._sort(key=key, cmp=cmp, reverse=reverse)
        return _IntermediateIteratorChain(iterator)

    def _sort(self, key=None, cmp=None, reverse=False):
        if key is None and cmp is not None:
            key = functools.cmp_to_key(cmp)
        return iter(sorted(self._iterator, key=key, reverse=reverse))

    def reverse(self):
        """
        Reverses the iterator.  The last item will be first, and the first item will be last.  This method is expensive because it must serialize all the values into a list.

        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        iterator = self._reverse()
        return _IntermediateIteratorChain(iterator)

    def _reverse(self):
        forward = list(self._iterator)
        return reversed(forward)

    # Termination methods
    def list(self):
        """
        Serializes the iterator chain into a `list` and returns it.

        :return: A list whose elements come from the iterator.
        """
        return list(self._iterator)

    def count(self):
        """
        Returns the number of elements in the iterator

        :return: An integer.
        """
        return sum(1 for _ in self._iterator)

    def first(self, default=None):
        """
        Returns just the first item in the iterator.  If the iterator is empty, the `default` is returned.

        :param default: Keyword.  Any value.
        :return: The first element.
        """
        return next(itertools.islice(self._iterator, 1), default)

    def last(self, default=None):
        """
         Returns just the last item in the iterator.  If the iterator is empty, the `default` is returned.

        :param default: Keyword.  Any value.
        :return: The last element.
        """
        try:
            end = collections.deque(self._iterator, maxlen=1).pop()
        except IndexError:
            end = default
        return end

    def max(self, default=None):
        """
        Returns the largest valued element in the iterator.  If the iterator is empty, the `default` is returned.

        :param default: Keyword.  Any value.
        :return: The largest element.
        """
        return max(self._iterator, default=default)

    def min(self, default=None):
        """
        Returns the smallest valued element in the iterator.  If the iterator is empty, the `default` is returned.

        :param default: Keyword.  Any value.
        :return: The smallest element.
        """
        return min(self._iterator, default=default)

    def sum(self, default=None):
        """
        Sums all the elements in the iterator together.  If any of the elements are un-summable, the `default` is returned.

        :param default: Keyword.  Any value.
        :return: The sum of all the elements.
        """
        try:
            total = sum(self._iterator)
        except TypeError:
            total = default
        return total

    def reduce(self, function, initial=None):
        """
        Applies the function to two elements in the iterator cumulatively.  Subsequent calls to `function` uses the previous return value from `function` as the first argument and the next element in the iterator as the second argument.  The final value is returned.  If `initial` is present, it is placed before the items of the sequence in the calculation, and serves as a default when the sequence is empty.

        :param function: A function that takes two arguments.
        :param initial: Keyword.  Any value.
        :return: The final reduced value.
        """
        if initial is None:
            return functools.reduce(function, self._iterator)
        else:
            return functools.reduce(function, self._iterator, initial)

    def for_each(self, function):
        """
        Executes `function` on every element in the iterator.  There is no return value.  If you are wanting to return a list of values based on the function, use `.map(function).list()`.

        :param function: A function that takes one argument and returns nothing.
        """
        for item in self._iterator:
            function(item)

    def all_match(self, function):
        """
        Returns `True` only if all the elements return `True` after applying the `function` to them.  Else returns `False`.

        :param function: A function that takes one argument and returns a boolean.
        :return: True or False
        """
        return all(map(function, self._iterator))

    def any_match(self, function):
        """
        Returns `True` if just one element return `True` after applying the `function` to it.  If all elements result in `False`, `False` is returned.

        :param function: A function that takes one argument and returns a boolean.
        :return: True or False
        """
        return any(map(function, self._iterator))

    def none_match(self, function):
        """
        Returns `True` only if all the elements return `False` after applying the `function` to them.  Else returns `True`.

        :param function: A function that takes one argument and returns a boolean.
        :return: True or False
        """
        return not self.any_match(function)
