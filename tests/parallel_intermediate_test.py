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
            print(submit_result)
            submit_future.set_result(submit_result)
        except Exception as exception:
            submit_future.set_exception(exception)

        return submit_future

    # def map(self, fn, *iterables, timeout=None, chunksize=1):
    #     super(SerialExecutor, self).map(fn, *iterables, timeout=timeout, chunksize=chunksize)

    def shutdown(self, wait=True):
        self.shutdown_called = True
        super(SerialExecutor, self).shutdown(wait=wait)


# Ensure that all public methods of _IntermediateIteratorChain are overloaded by _IntermediateParallelIteratorChain and are decorated by @shutdown_executor_on_exception
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


# Chain methods
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


# Test chunk size
def test_filter_with_specified_chunksize():
    test_iterable = [4, 3, 8, 5, 1]
    test_iterator = iter(test_iterable)
    test_object = _IntermediateParallelIteratorChain(test_iterator, SerialExecutor(), chunksize=2)
    test_lambda = lambda item: item > 4

    new_intermediate = test_object.filter(test_lambda)

    assert new_intermediate.list() == list(filter(test_lambda, [4, 3, 8, 5, 1]))


def test_filter_with_specified_chunksize_on_specific_method():
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
