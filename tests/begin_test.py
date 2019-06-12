from iterator_chain import begin


def test_from_iterable():
    test_iterable = [4, 3, 8, 5, 1]

    new_intermediate = begin.from_iterable(test_iterable)

    assert list(new_intermediate._iterator) == test_iterable
