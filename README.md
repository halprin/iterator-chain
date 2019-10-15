# iterator-chain
Chain together lazily computed modifications to iterators.

One normally needs to do the following
```python
list(map(lambda element: element / 3,
filter(lambda element: element > 32,
map(lambda element: element * 2, [5, 78, 12, 26]))))
```

Instead do this
```python
iterator_chain.from_iterable([5, 78, 12, 26]) \
.map(lambda element: element * 2) \
.filter(lambda element: element > 32) \
.map(lambda element: element / 3).list()
```

It allows the developer to read the code in a more natural fashion: from left to right and from top to bottom.  The
developer no longer needs to "unwrap" the functions to understand the logic.

## Install
Include `iterator-chain` in your `requirements.txt` file and/or use `pip` to install it.
```bash
$ pip install iterator-chain
```

## API
Start by importing the package.
```python
import iterator_chain
```

### Start the chain
To start the chain, use the `from_iterable` or `from_iterable_parallel` function.  They take an iterable.
```python
an_iterable = [5, 78, 12, 26]
chain = iterator_chain.from_iterable(an_iterable)
parallel_chain = iterator_chain.from_iterable_parallel(an_iterable)
```

| Function | Arguments | Description |
| --- | --- | --- |
| `from_iterable` | • `iterable` - An iterable to be used in the iterator chain | Starts the iterator chain with the supplied iterable.  Chaining and terminating methods can now be called on the result. |
| `from_iterable_parallel` | • `iterable` - An iterable to be used in the iterator chain<br/>• `chunksize` - Keyword.  How big of chunks to split the iterator up across the parallel execution units.  If unspecified or None, the chunk size will start at 1 and send that many elements to each execution unit.  The chunk size will then increment in powers of two and send that many items to each execution unit.  This is repeated until the iterator is exhausted.  This value is used as the default chunksize for all the following parallel based methods.  A specific parallel based method's chunksize can be overrided by supplying the `chunksize` keyword to that method. | Starts the iterator chain with the supplied iterable.  Chaining and terminating methods can now be called on the result.  Certain chaining and terminating methods will occur in parallel.  Parallel means separate processes to get around Python's GIL. |


### Continuing the chain
From there, one can call a plethora of additional methods to modify the iterable passed in originally.  The methods are
outlined below.  The methods fall into one of two categories: chaining or terminating.

- Chaining methods apply some modification to the elements in the iterator, but keeps the chain alive.
This allows additional chaining methods to be subsequently called on the result.
Because modifications are lazily computed, none of the modifications from chaining methods are applied until _after_ a terminating method is
called.
- Terminating methods also apply some modification, requests some information, or executes something on the elements in the iterator.  They stop the chaining by returning
an actual value.  This value will depend on all the previous chaining methods being executed first.

#### Chaining methods
| Method | Arguments | Description |
| --- | --- | --- |
| `map` | • `function` - A function that takes a single argument | Will run the `function` across all the elements in the iterator. |
| `filter` | • `function` - A function that takes a single argument | Will run the `function` on every element.  `function` should return a truthy or falsy value.  On true, the element will stay; on false, the element will be removed. |
| `skip` | • `number` - An integer | The `number` number of elements will be skipped over and effectively removed. |
| `distinct` |  | Any duplicates will be removed. |
| `limit` | • `max_size` - An integer | The iterator will stop after `max_size` elements.  Any elements afterward are effectively removed. |
| `flatten` |  | Any element that is an iterable itself will have its elements iterated over first before continuing with the remaining elements.  Strings (`str`) do not count as an iterable for this method.  Dictionaries flatten to its item tuples. |
| `sort` | • `key` - Keyword.  A function of one argument that is used to extract a comparison key from each element<br/>• `cmp` - Keyword.  A Python 2.x "cmp" function that takes two arguments<br/>• `reverse` - Keyword.  If set to `True`, the elements will be sorted in the reverse order | Sorts the iterator based on the elements' values.  Use `key` or `cmp` to make a custom comparison.  If `key` is specified, `cmp` cannot be used.  This method is expensive because it must serialize all the values into a sequence. |
| `reverse` |  | Reverses the iterator.  The last item will be first, and the first item will be last.  This method is expensive because it must serialize all the values into a list. |

##### Parallel Versions
| Method | Arguments | Description |
| --- | --- | --- |
| `map` | • `function` - A function that takes a single argument<br/>• `chunksize` - Keyword.  Overrides the chunksize supplied to the original `from_iterable_parallel`  | Will run the `function` across all the elements in the iterator in parallel. |
| `filter` | • `function` - A function that takes a single argument<br/>• `chunksize` - Keyword.  Overrides the chunksize supplied to the original `from_iterable_parallel` | Will run the `function` on every element in parallel.  `function` should return a truthy or falsy value.  On true, the element will stay; on false, the element will be removed. |

#### Terminating methods
| Method | Arguments | Description |
| --- | --- | --- |
| `list` |  | Serializes the iterator chain into a `list` and returns it. |
| `count` |  | Returns the number of elements in the iterator. |
| `first` | • `default` - Keyword.  Any value. | Returns just the first item in the iterator.  If the iterator is empty, the `default` is returned. |
| `last` | • `default` - Keyword.  Any value. | Returns just the last item in the iterator.  If the iterator is empty, the `default` is returned. |
| `max` | • `default` - Keyword.  Any value. | Returns the largest valued element in the iterator.  If the iterator is empty, the `default` is returned. |
| `min` | • `default` - Keyword.  Any value. | Returns the smallest valued element in the iterator.  If the iterator is empty, the `default` is returned. |
| `sum` | • `default` - Keyword.  Any value. | Sums all the elements in the iterator together.  If any of the elements are un-summable, the `default` is returned. |
| `reduce` | • `function` - A function that takes two arguments | Applies the function to two elements in the iterator cumulatively.  Subsequent calls to `function` uses the previous return value from `function` as the first argument and the next element in the iterator as the second argument.  The final value is returned. |
| `for_each` | • `function` - A function that takes one argument and returns nothing | Executes `function` on every element in the iterator.  There is no return value.  If you are wanting to return a list of values based on the function, use `.map(_function_).list()`. |
| `all_match` | • `function` - A function that takes one argument and returns a boolean | Returns `True` only if _all_ the elements return `True` after applying the `function` to them.  Else returns `False`. |
| `any_match` | • `function` - A function that takes one argument and returns a boolean | Returns `True` if just one element return `True` after applying the `function` to it.  If all elements result in `False`, `False` is returned. |
| `none_match` | • `function` - A function that takes one argument and returns a boolean | Returns `True` only if _all_ the elements return `False` after applying the `function` to them.  Else returns `True`. |

##### Parallel Versions
| Method | Arguments | Description |
| --- | --- | --- |
| `for_each` | • `function` - A function that takes one argument and returns nothing<br/>• `chunksize` - Keyword.  Overrides the chunksize supplied to the original `from_iterable_parallel` | Executes `function` on every element in the iterator in parallel.  There is no return value.  If you are wanting to return a list of values based on the function, use `.map(function).list()`. |

## Examples
```python
import iterator_chain
an_iterable = [5, 78, 12, 26]
iterator_chain.from_iterable(an_iterable) \  #starts the chain
    .map(lambda element: element * 2) \  #multiplies every element by two: [10, 156, 24, 52]
    .filter(lambda element: element > 32) \  #keeps any element greater than 32: [156, 52]
    .map(lambda element: element / 3) \ #divides every element by three: [52.0, 17.333333333333332]
    .list()  #and finally returns a list of the result for later use in your application: [52.0, 17.333333333333332]
```
