from concurrent.futures import Executor
from concurrent.futures import Future
import inspect
from iterator_chain.parallel_intermediate import _IntermediateParallelIteratorChain
from iterator_chain.intermediate import _IntermediateIteratorChain


class SerialExecutor(Executor):
    def __init__(self):
        self.shutdown_called = False

    def submit(self, fn, *args, **kwargs):
        submit_future = Future()

        try:
            submit_result = fn(*args, **kwargs)
            submit_future.set_result(submit_result)
        except Exception as exception:
            submit_future.set_exception(exception)

        return submit_future

    # def map(self, fn, *iterables, timeout=None, chunksize=1):
    #     super(SerialExecutor, self).map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait=True):
        self.shutdown_called = True
        super(SerialExecutor, self).shutdown(wait=wait)


# Ensure that all public methods of _IntermediateIteratorChain are overloaded by _IntermediateParallelIteratorChain
def test_correct_overloading():
    parent_class_methods = {method[0]: method[1] for method in inspect.getmembers(_IntermediateIteratorChain, predicate=inspect.isfunction)}
    class_methods = {method[0]: method[1] for method in inspect.getmembers(_IntermediateParallelIteratorChain, predicate=inspect.isfunction)}

    for parent_method_name in parent_class_methods:
        if parent_method_name[0] == '_':
            continue
        if class_methods.get(parent_method_name, None) is None:
            raise Exception('{} is not inherited by _IntermediateParallelIteratorChain'.format(parent_method_name))
        elif class_methods[parent_method_name] == parent_class_methods[parent_method_name]:
            raise Exception('{} is not overloaded by _IntermediateParallelIteratorChain'.format(parent_method_name))


# Parallel tests
def test_executor_shutdowns_when_no_terminating_method_called():
    executor = SerialExecutor()

    def inner_scope():
        test_iterable = [4, 3, 8, 5, 1]
        test_iterator = iter(test_iterable)
        test_object = _IntermediateParallelIteratorChain(test_iterator, executor)

        new_intermediate = test_object.map(lambda item: item * item)

    inner_scope()

    assert executor.shutdown_called is True


def test_executor_shutdowns_when_exception_raised():
    executor = SerialExecutor()

    def exception_function(item):
        raise Exception('kaboom')

    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, executor)

    try:
        new_intermediate = test_object.map(exception_function).list()
    except:
        pass

    assert executor.shutdown_called is True


# Chain methods parallel
def test_map():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    new_intermediate = test_object.map(lambda item: item * item)

    assert new_intermediate.list() == [item * item for item in test_iterable]


def test_filter():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())
    test_lambda = lambda item: item > 4

    new_intermediate = test_object.filter(test_lambda)

    assert new_intermediate.list() == list(filter(test_lambda, [4, 3, 8, 5, 1]))


# Chain methods work the same as serial
def test_skip():
    test_iterable = [4, 3, 8, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.skip(3)
    new_parallel_intermediate = test_parallel_object.skip(3)

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_distinct():
    test_iterable = [4, 3, 4, 5, 1, 3, 4]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.distinct()
    new_parallel_intermediate = test_parallel_object.distinct()

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_limit():
    test_iterable = [4, 3, 8, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.limit(3)
    new_parallel_intermediate = test_parallel_object.limit(3)

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_flatten():
    test_iterable = [[4, 3], 'DogCow', 5, {'dogCow': 'Moof', 'meep': 'moop'}]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.flatten()
    new_parallel_intermediate = test_parallel_object.flatten()

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_sort():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.sort()
    new_parallel_intermediate = test_parallel_object.sort()

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_sort_reverse():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.sort(reverse=True)
    new_parallel_intermediate = test_parallel_object.sort(reverse=True)

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_sort_with_key():
    test_iterable = [{'inner': 8}, {'inner': 2}, {'inner': 6}, {'inner': 3}, {'inner': 9}]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_key = lambda item: item['inner']

    new_serial_intermediate = test_serial_object.sort(key=test_key)
    new_parallel_intermediate = test_parallel_object.sort(key=test_key)

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def _test_cmp(first, second):
    if first['inner'] > second['inner']:
        return 1
    elif first['inner'] == second['inner']:
        return 0
    else:
        return -1


def test_sort_with_cmp():
    test_iterable = [{'inner': 8}, {'inner': 2}, {'inner': 6}, {'inner': 3}, {'inner': 9}]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.sort(cmp=_test_cmp)
    new_parallel_intermediate = test_parallel_object.sort(cmp=_test_cmp)

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


def test_reverse():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    new_serial_intermediate = test_serial_object.reverse()
    new_parallel_intermediate = test_parallel_object.reverse()

    assert new_parallel_intermediate.list() == new_serial_intermediate.list()


# Terminating methods parallel
def test_for_each():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())
    test_parallel_output = []

    def function_test(item):
        test_parallel_output.append(item)

    test_object.for_each(function_test)

    assert test_parallel_output == test_iterable


# Test chunk size
def test_with_specified_chunksize():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor(), chunksize=2)
    test_lambda = lambda item: item > 4

    new_intermediate = test_object.filter(test_lambda)

    assert new_intermediate.list() == list(filter(test_lambda, [4, 3, 8, 5, 1]))


def test_with_specified_chunksize_on_specific_method():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())
    test_lambda = lambda item: item > 4

    new_intermediate = test_object.filter(test_lambda, chunksize=2)

    assert new_intermediate.list() == list(filter(test_lambda, [4, 3, 8, 5, 1]))


# Termination methods
def test_list():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_list = test_object.list()

    assert actual_list == test_iterable


def test_count():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_count = test_object.count()

    assert actual_count == len(test_iterable)


def test_first():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_first = test_object.first()

    assert actual_first == test_iterable[0]


def test_first_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_first = test_object.first('Moof')

    assert actual_first == test_iterable[0]


def test_first_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())
    test_default = 'Moof'

    actual_first = test_object.first(test_default)

    assert actual_first == test_default


def test_last():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_last = test_object.last()

    assert actual_last == test_iterable[-1]


def test_last_with_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())

    actual_last = test_object.last('Moof')

    assert actual_last == test_iterable[-1]


def test_last_with_default():
    test_iterable = []
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor())
    test_default = 'Moof'

    actual_last = test_object.last(test_default)

    assert actual_last == test_default


def test_max():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.max()
    parallel_value = test_parallel_object.max()

    assert parallel_value == serial_value


def test_max_with_default():
    test_iterable = []
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.max(default=test_default)
    parallel_value = test_parallel_object.max(default=test_default)

    assert parallel_value == serial_value


def test_max_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.max(default=test_default)
    parallel_value = test_parallel_object.max(default=test_default)

    assert parallel_value == serial_value


def test_min():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.min()
    parallel_value = test_parallel_object.min()

    assert parallel_value == serial_value


def test_min_with_default():
    test_iterable = []
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.min(default=test_default)
    parallel_value = test_parallel_object.min(default=test_default)

    assert parallel_value == serial_value


def test_min_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.min(default=test_default)
    parallel_value = test_parallel_object.min(default=test_default)

    assert parallel_value == serial_value


def test_sum():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.sum()
    parallel_value = test_parallel_object.sum()

    assert parallel_value == serial_value


def test_sum_with_default():
    test_iterable = ['D', 'o', 'g', 'C', 'o', 'w']
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.sum(default=test_default)
    parallel_value = test_parallel_object.sum(default=test_default)

    assert parallel_value == serial_value


def test_sum_default_not_used():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())
    test_default = 'Moof'

    serial_value = test_serial_object.sum(default=test_default)
    parallel_value = test_parallel_object.sum(default=test_default)

    assert parallel_value == serial_value


def test_reduce():
    test_iterable = [4, 3, 8, 5, 6]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.reduce(lambda first, second: first * second)
    parallel_value = test_parallel_object.reduce(lambda first, second: first * second)

    assert parallel_value == serial_value


def test_reduce_with_initial():
    test_iterable = [4, 3, 8, 5, 6]
    test_initial = 26
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.reduce(lambda first, second: first * second, initial=test_initial)
    parallel_value = test_parallel_object.reduce(lambda first, second: first * second, initial=test_initial)

    assert parallel_value == serial_value


def test_all_match_true():
    test_iterable = [4, 3, 8, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.all_match(lambda item: item < 26)
    parallel_value = test_parallel_object.all_match(lambda item: item < 26)

    assert parallel_value == serial_value


def test_all_match_false():
    test_iterable = [4, 3, 27, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.all_match(lambda item: item < 26)
    parallel_value = test_parallel_object.all_match(lambda item: item < 26)

    assert parallel_value == serial_value


def test_any_match_true():
    test_value = 8
    test_iterable = [4, 3, test_value, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.any_match(lambda item: item == test_value)
    parallel_value = test_parallel_object.any_match(lambda item: item == test_value)

    assert parallel_value == serial_value


def test_any_match_false():
    test_value = 26
    test_iterable = [4, 3, 8, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.any_match(lambda item: item == test_value)
    parallel_value = test_parallel_object.any_match(lambda item: item == test_value)

    assert parallel_value == serial_value


def test_none_match_false():
    test_value = 8
    test_iterable = [4, 3, test_value, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.none_match(lambda item: item == test_value)
    parallel_value = test_parallel_object.none_match(lambda item: item == test_value)

    assert parallel_value == serial_value


def test_none_match_true():
    test_value = 26
    test_iterable = [4, 3, 8, 5, 1]
    test_serial_iterator = iter(test_iterable)
    test_parallel_iterator = iter(test_iterable)
    test_serial_object = _IntermediateIteratorChain(test_serial_iterator)
    test_parallel_object = _IntermediateParallelIteratorChain(test_parallel_iterator, SerialExecutor())

    serial_value = test_serial_object.none_match(lambda item: item == test_value)
    parallel_value = test_parallel_object.none_match(lambda item: item == test_value)

    assert parallel_value == serial_value

