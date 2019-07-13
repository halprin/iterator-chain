from concurrent.futures import ProcessPoolExecutor
from iterator_chain.intermediate import _IntermediateIteratorChain
from iterator_chain.parallel_itermediate import _IntermediateParallelIteratorChain


def from_iterable(iterable):
    iterator = iter(iterable)
    return _IntermediateIteratorChain(iterator)


def from_iterable_parallel(iterable, chunksize=None):
    iterator = iter(iterable)
    executor = ProcessPoolExecutor()
    return _IntermediateParallelIteratorChain(iterator, executor, chunksize=chunksize)
