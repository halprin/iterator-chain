from iterator_chain.intermediate import _IntermediateIteratorChain


def from_iterable(iterable):
    iterator = iter(iterable)
    return _IntermediateIteratorChain(iterator)
