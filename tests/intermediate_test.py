from iterator_chain.intermediate import _IntermediateIteratorChain


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


def test_reduce_with_initial():
    test_iterable = [4, 3, 8, 5, 6]
    test_initial = 26
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_reduction = test_object.reduce(lambda first, second: first * second, initial=test_initial)

    assert actual_reduction == test_initial * test_iterable[0] * test_iterable[1] * test_iterable[2] * test_iterable[3] * test_iterable[4]


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

    actual_min = test_object.min()

    assert actual_min == min(test_iterable)


def test_min_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_min = test_object.min('Moof')

    assert actual_min == min(test_iterable)


def test_min_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_min = test_object.min(test_default)

    assert actual_min == test_default


def test_sum():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_sum = test_object.sum()

    assert actual_sum == sum(test_iterable)


def test_sum_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_sum = test_object.sum('Moof')

    assert actual_sum == sum(test_iterable)


def test_sum_with_default():
    test_iterable = ['D', 'o', 'g', 'C', 'o', 'w']
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_sum = test_object.sum(test_default)

    assert actual_sum == test_default


def test_last():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_last = test_object.last()

    assert actual_last == test_iterable[-1]


def test_last_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_last = test_object.last('Moof')

    assert actual_last == test_iterable[-1]


def test_last_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_default = 'Moof'

    actual_last = test_object.last(test_default)

    assert actual_last == test_default


def test_for_each():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_call = []
    test_lambda = lambda item: test_call.append(item)

    test_object.for_each(test_lambda)

    assert test_call == test_iterable


def test_reverse():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_reverse = test_object.reverse().list()

    assert actual_reverse == list(reversed(test_iterable))


def test_sort():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_sort = test_object.sort().list()

    assert actual_sort == sorted(test_iterable)


def test_sort_reverse():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_sort = test_object.sort(reverse=True).list()

    assert actual_sort == sorted(test_iterable, reverse=True)


def test_sort_with_key():
    test_iterable = [{'inner': 8}, {'inner': 2}, {'inner': 6}, {'inner': 3}, {'inner': 9}]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_key = lambda item: item['inner']

    actual_sort = test_object.sort(key=test_key).list()

    assert actual_sort == sorted(test_iterable, key=test_key)


def _test_cmp(first, second):
    if first['inner'] > second['inner']:
        return 1
    elif first['inner'] == second['inner']:
        return 0
    else:
        return -1


def test_sort_with_cmp():
    test_iterable = [{'inner': 8}, {'inner': 2}, {'inner': 6}, {'inner': 3}, {'inner': 9}]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)
    test_key = lambda item: item['inner']

    actual_sort = test_object.sort(cmp=_test_cmp).list()

    assert actual_sort == sorted(test_iterable, key=test_key)


def test_flatten():
    test_iterable = [[4, 3], 'DogCow', 5, {'dogCow': 'Moof', 'meep': 'moop'}]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateIteratorChain(test_iterator)

    actual_flatten = test_object.flatten().list()

    assert actual_flatten == [4, 3, 'DogCow', 5, ('dogCow', 'Moof'), ('meep', 'moop')]
