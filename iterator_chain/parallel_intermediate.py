import functools
from iterator_chain.intermediate import _IntermediateIteratorChain
import collections
import os
import itertools
from functools import wraps


def shutdown_executor_on_exception(original_function):
    @wraps(original_function)
    def wrapper(self, *args, **kwargs):
        try:
            return original_function(self, *args, **kwargs)
        except Exception as exception:
            self._executor.shutdown(wait=True)
            raise exception

    return wrapper


class _IntermediateParallelIteratorChain(_IntermediateIteratorChain):
    def __init__(self, iterator, executor, chunksize=None):
        super(_IntermediateParallelIteratorChain, self).__init__(iterator)
        self._executor = executor
        self._chunksize = chunksize
        self._chain_method_called = False

    # Chain methods
    @shutdown_executor_on_exception
    def map(self, function, chunksize=None):
        """
        Will run the `function` across all the elements in the iterator in parallel.

        :param function: A function that takes a single argument.
        :param chunksize: Overrides the chunksize supplied to the original `from_iterable_parallel`.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        chunksize = chunksize or self._chunksize
        self._chain_method_called = True

        iterator_of_results = _ParallelExecutionIterator(self._iterator, function, self._executor, chunksize=chunksize)

        return _IntermediateParallelIteratorChain(iterator_of_results, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def filter(self, function, chunksize=None):
        """
        Will run the `function` on every element in parallel.  `function` should return a truthy or falsy value.  On true, the element will stay; on false, the element will be removed.

        :param function: A function that takes a single argument.
        :param chunksize: Overrides the chunksize supplied to the original `from_iterable_parallel`.
        :return: An intermediate object that subsequent chaining and terminating methods can be called on.
        """
        chunksize = chunksize or self._chunksize
        self._chain_method_called = True

        partial_filter_helper = functools.partial(self._filter_helper, function)
        iterator_of_results = _ParallelExecutionIterator(self._iterator, partial_filter_helper, self._executor, chunksize=chunksize)
        filtered_results_iterator = filter(lambda item_tuple: item_tuple[1], iterator_of_results)
        filtered_original_item_iterator = map(lambda item_tuple: item_tuple[0], filtered_results_iterator)

        return _IntermediateParallelIteratorChain(filtered_original_item_iterator, self._executor, chunksize=self._chunksize)

    @staticmethod
    def _filter_helper(function, item):
        true_or_false = function(item)
        return item, true_or_false

    @shutdown_executor_on_exception
    def skip(self, number):
        self._chain_method_called = True
        iterator = self._skip(number)
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def distinct(self):
        self._chain_method_called = True
        iterator = self._distinct()
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def limit(self, max_size):
        self._chain_method_called = True
        iterator = self._limit(max_size)
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def flatten(self):
        self._chain_method_called = True
        iterator = self._flatten(self._iterator)
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def sort(self, key=None, cmp=None, reverse=False):
        self._chain_method_called = True
        iterator = self._sort(key=key, cmp=cmp, reverse=reverse)
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    @shutdown_executor_on_exception
    def reverse(self):
        self._chain_method_called = True
        iterator = self._reverse()
        return _IntermediateParallelIteratorChain(iterator, self._executor, chunksize=self._chunksize)

    # Termination methods
    @shutdown_executor_on_exception
    def list(self):
        serialized = super(_IntermediateParallelIteratorChain, self).list()
        return serialized

    @shutdown_executor_on_exception
    def count(self):
        count = super(_IntermediateParallelIteratorChain, self).count()
        return count

    @shutdown_executor_on_exception
    def first(self, default=None):
        first = super(_IntermediateParallelIteratorChain, self).first(default)
        return first

    @shutdown_executor_on_exception
    def last(self, default=None):
        last = super(_IntermediateParallelIteratorChain, self).last(default)
        return last

    @shutdown_executor_on_exception
    def max(self, default=None):
        max = super(_IntermediateParallelIteratorChain, self).max(default)
        return max

    @shutdown_executor_on_exception
    def min(self, default=None):
        min = super(_IntermediateParallelIteratorChain, self).min(default)
        return min

    @shutdown_executor_on_exception
    def sum(self, default=None):
        sum = super(_IntermediateParallelIteratorChain, self).sum(default)
        return sum

    @shutdown_executor_on_exception
    def reduce(self, function, initial=None):
        reduce = super(_IntermediateParallelIteratorChain, self).reduce(function, initial=initial)
        return reduce

    @shutdown_executor_on_exception
    def for_each(self, function, chunksize=None):
        """
        Executes `function` on every element in the iterator in parallel.  There is no return value.  If you are wanting to return a list of values based on the function, use `.map(function).list()`.

        :param function: A function that takes one argument and returns nothing.
        :param chunksize: Overrides the chunksize supplied to the original `from_iterable_parallel`.
        """
        chunksize = chunksize or self._chunksize

        iterator_of_results = _ParallelExecutionIterator(self._iterator, function, self._executor, chunksize=chunksize)
        list(iterator_of_results)

    @shutdown_executor_on_exception
    def all_match(self, function):
        all_match = super(_IntermediateParallelIteratorChain, self).all_match(function)
        return all_match

    @shutdown_executor_on_exception
    def any_match(self, function):
        any_match = super(_IntermediateParallelIteratorChain, self).any_match(function)
        return any_match

    @shutdown_executor_on_exception
    def none_match(self, function):
        none_match = super(_IntermediateParallelIteratorChain, self).none_match(function)
        return none_match

    def __del__(self):
        if not self._chain_method_called:
            # we were the last chain method, we are in charge of shutting down the executor
            self._executor.shutdown(wait=True)


class _ParallelExecutionIterator(collections.abc.Iterator):
    def __init__(self, iterator, function, executor, chunksize=None):
        self._input_iterator = iterator
        self._function = function
        self._executor = executor
        self._executed = False
        self._output_iterator = None
        self._chunksize = chunksize

    def __iter__(self):
        """
        Returns itself.

        :return: Itself
        """
        return self

    def __next__(self):
        """
        Upon first invocation, the function executes against every item in the iterator in parallel.  Once complete,
        the first mapped value is returned.  Subsequent invocations immediately return the next mapped value.

        :return: The next mapped value after executing the function against every item in the iterator in a parallel
        fashion.
        """
        if not self._executed:
            self._executed = True
            self._execute()

        return next(self._output_iterator)

    def _execute(self):
        if self._chunksize is not None:
            self._output_iterator = self._executor.map(self._function, self._input_iterator, chunksize=self._chunksize)
        else:
            self._output_iterator = self._map_successively_larger_slices(self._executor, self._function, self._input_iterator)

    @classmethod
    def _map_successively_larger_slices(cls, executor, function, input_iterator):
        """
        Successively slices more and more items from the iterator and executes the function against them until the
        iterator is exhausted.

        :param executor: The executor to use
        :param function: The function to execute against every item in the iterator.
        :param input_iterator: The iterator to run the function against.
        :return: An iterator who's values have been transformed by the function.
        """
        cpu_count = os.cpu_count() or 1

        constructed_output_iterator = iter([])

        for chunksize in cls._power_of_two_range(1):
            miniature_input_iterator = itertools.islice(input_iterator, chunksize * cpu_count)
            list_of_miniature_input_iterator = [miniature_input_iterator]
            if cls._iterator_is_empty(list_of_miniature_input_iterator):
                break
            miniature_input_iterator = list_of_miniature_input_iterator[0]
            miniature_output_iterator = executor.map(function, miniature_input_iterator, chunksize=chunksize)
            constructed_output_iterator = itertools.chain(constructed_output_iterator, miniature_output_iterator)

        return constructed_output_iterator

    @staticmethod
    def _power_of_two_range(start):
        """
        A generator that continually returns the next power of two value.
        E.g. 1, 2, 4, 8, 16, 32, etc.

        :param start: The value to start at.
        """
        while True:
            yield start
            start <<= 1

    @staticmethod
    def _iterator_is_empty(list_with_iterator):
        """
        Checks the iterator whether it is empty or not.  It does this by "tasting" the iterator and reconstructing it
        if it is not empty.

        :param list_with_iterator: A list with a single item: the iterator to test.
        :return: True if the iterator is empty, False if the iterator is not empty.
        """
        try:
            first_item = next(list_with_iterator[0])
            list_with_iterator[0] = itertools.chain([first_item], list_with_iterator[0])
            return False
        except StopIteration:
            return True
