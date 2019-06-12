import iterator_chain


def test_init_direct_reference():
    assert iterator_chain.from_iterable == iterator_chain.begin.from_iterable
