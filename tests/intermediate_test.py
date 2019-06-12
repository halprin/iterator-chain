from iterator_chain.intermediate import _IntermediateIteratorChain


# Termination tests
def test_list():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_list = test_object.list()

    assert actual_list == test_iterable


def test_first():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_first = test_object.first()

    assert actual_first == test_iterable[0]


def test_first_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_first = test_object.first('Moof')

    assert actual_first == test_iterable[0]


def test_first_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_first = test_object.first(test_default)

    assert actual_first == test_default


# Chain tests
def test_map():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    new_intermediate = test_object.map(lambda item: item * item)

    assert new_intermediate.list() == [item * item for item in test_iterable]


def test_skip():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    new_intermediate = test_object.skip(3)

    assert new_intermediate.list() == test_iterable[3:]


def test_filter():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_lambda = lambda item: item > 4

    new_intermediate = test_object.filter(test_lambda)

    assert new_intermediate.list() == list(filter(test_lambda, [4, 3, 8, 5, 1]))


def test_limit():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    new_intermediate = test_object.limit(3)

    assert new_intermediate.list() == test_iterable[:3]


def test_distinct():
    test_iterable = [4, 3, 4, 5, 1, 3, 4]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    new_intermediate = test_object.distinct()

    assert new_intermediate.list() == [4, 3, 5, 1]
