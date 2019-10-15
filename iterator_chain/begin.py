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
    """
    Starts the iterator chain with the supplied iterable.  Chaining and terminating methods can now be called on the result.  Certain chaining and terminating methods will occur in parallel.  Parallel means separate processes to get around Python's GIL.

    :param iterable: An iterable to be used in the iterator chain.
    :param chunksize: How big of chunks to split the iterator up across the parallel execution units.  If unspecified or None, the chunk size will start at 1 and send that many elements to each execution unit.  The chunk size will then increment in powers of two and send that many items to each execution unit.  This is repeated until the iterator is exhausted.  This value is used as the default chunksize for all the following parallel based methods.  A specific parallel based method's chunksize can be overrided by supplying the `chunksize` keyword to that method.
    :return: An intermediate object that subsequent chaining and terminating methods can be called on.
    """
    iterator = iter(iterable)
    executor = ProcessPoolExecutor()
    return _IntermediateParallelIteratorChain(iterator, executor, chunksize=chunksize)
