from concurrent.futures import ProcessPoolExecutor
from iterator_chain.intermediate import _IntermediateIteratorChain
from iterator_chain.parallel_intermediate import _IntermediateParallelIteratorChain


def from_iterable(iterable):
    """
    Starts the iterator chain with the supplied iterable.  Chaining and terminating methods can now be called on the result.

    :param iterable: An iterable to be used in the iterator chain.
    :return: An intermediate object that subsequent chaining and terminating methods can be called on.
    """
    iterator = iter(iterable)
    return _IntermediateIteratorChain(iterator)


def from_iterable_parallel(iterable, chunksize=None):
    iterator = iter(iterable)
    executor = ProcessPoolExecutor()
    return _IntermediateParallelIteratorChain(iterator, executor, chunksize=chunksize)
