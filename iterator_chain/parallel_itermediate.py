import functools
from iterator_chain.intermediate import _IntermediateIteratorChain
import collections
import os
import itertools


class _IntermediateParallelIteratorChain(_IntermediateIteratorChain):
    def __init__(self, iterator, executor, chunksize=None):
        super(_IntermediateParallelIteratorChain, self).__init__(iterator)
        self._executor = executor
        self._chunksize = chunksize

    # Chain methods
    def map(self, function, chunksize=None):
        chunksize = chunksize or self._chunksize

        iterator_of_results = _ParallelExecutionIterator(self._iterator, function, self._executor, chunksize=chunksize)

        return _IntermediateParallelIteratorChain(iterator_of_results, self._executor)

    def filter(self, function, chunksize=None):
        chunksize = chunksize or self._chunksize

        partial_filter_helper = functools.partial(self._filter_helper, function)
        iterator_of_results = _ParallelExecutionIterator(self._iterator, partial_filter_helper, self._executor, chunksize=chunksize)
        filtered_results_iterator = filter(lambda item_tuple: item_tuple[1], iterator_of_results)
        filtered_original_item_iterator = map(lambda item_tuple: item_tuple[0], filtered_results_iterator)

        return _IntermediateParallelIteratorChain(filtered_original_item_iterator, self._executor)

    @staticmethod
    def _filter_helper(function, item):
        true_or_false = function(item)
        return item, true_or_false

    # Termination methods
    def list(self):
        serialized = super(_IntermediateParallelIteratorChain, self).list()
        self._executor.shutdown(wait=True)
        return serialized

    def count(self):
        count = super(_IntermediateParallelIteratorChain, self).count()
        self._executor.shutdown(wait=True)
        return count

    def first(self, default=None):
        first = super(_IntermediateParallelIteratorChain, self).first(default)
        self._executor.shutdown(wait=True)
        return first

    def last(self, default=None):
        last = super(_IntermediateParallelIteratorChain, self).last(default)
        self._executor.shutdown(wait=True)
        return last


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
        :param function: The function to execute against every item in the iterator
        :param input_iterator: The iterator to run the function against.
        :return: An iterator who's values have been transformed by the function.
        """
        cpu_count = os.cpu_count() or 1

        constructed_output_iterator = iter([])

        for chunksize in cls._power_of_two_range(1):
            miniature_input_iterator = itertools.islice(input_iterator, chunksize * cpu_count)
            if cls._iterator_is_empty([miniature_input_iterator]):
                break
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

