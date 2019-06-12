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


def test_reduce():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_reduction = test_object.reduce(lambda first, second: first * second)

    assert actual_reduction == test_iterable[0] * test_iterable[1] * test_iterable[2] * test_iterable[3] * test_iterable[4]


def test_any_match_true():
    test_value = 8
    test_iterable = [4, 3, test_value, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_match = test_object.any_match(lambda item: item == test_value)

    assert actual_match == (test_value in test_iterable)


def test_any_match_false():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    test_value = 26
    actual_match = test_object.any_match(lambda item: item == test_value)

    assert actual_match == (test_value in test_iterable)


def test_none_match_false():
    test_value = 8
    test_iterable = [4, 3, test_value, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_none_match = test_object.none_match(lambda item: item == test_value)

    assert actual_none_match == (test_value not in test_iterable)


def test_none_match_true():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    test_value = 26
    actual_none_match = test_object.none_match(lambda item: item == test_value)

    assert actual_none_match == (test_value not in test_iterable)


def test_all_match_true():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_match = test_object.all_match(lambda item: item < 26)

    assert actual_match is True


def test_all_match_false():
    test_iterable = [4, 3, 27, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_match = test_object.all_match(lambda item: item < 26)

    assert actual_match is False


def test_count():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_count = test_object.count()

    assert actual_count == len(test_iterable)


def test_max():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_max = test_object.max()

    assert actual_max == max(test_iterable)


def test_max_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_max = test_object.max('Moof')

    assert actual_max == max(test_iterable)


def test_max_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_max = test_object.max(test_default)

    assert actual_max == test_default


def test_min():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_max = test_object.min()

    assert actual_max == min(test_iterable)


def test_min_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_max = test_object.min('Moof')

    assert actual_max == min(test_iterable)


def test_min_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_max = test_object.min(test_default)

    assert actual_max == test_default

