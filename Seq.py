import __builtin__
import itertools as _itertools
import functools as _functools
import collections as _collections
import operator as _operator


class Seq:

    def __init__(self, function):
        self.function = function

    def __rrshift__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Seq(lambda x: self.function(x, *args, **kwargs))


# sequence initialization methods --------------------

def unfold(function, initial):
    x = initial
    while x is not None:
        w, x = function(x)
        yield w

# sequence methods ------------------------------------

@Seq
def sum(x):
    return __builtin__.sum(x)


@Seq
def filter(sequence, function):
    return _itertools.ifilter(function, sequence)


@Seq
def takeWhile(sequence, function):
    return _itertools.takewhile(function, sequence)


@Seq
def map(sequence, function):
    if isinstance(sequence, _collections.Iterable):
        return _itertools.imap(function, sequence)
    else:
        return function(sequence)


@Seq
def toList(sequence):
    return list(sequence)


@Seq
def take(sequence, n):
    return list(_itertools.islice(sequence, n))


@Seq
def max(sequence):
    return __builtin__.max(sequence)


@Seq
def reduce(sequence, function):
    return _functools.reduce(function, sequence)


@Seq
def window(sequence, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(sequence)
    result = tuple(_itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

@Seq
def product(sequence):
    return _functools.reduce(_operator.mul, sequence)


@Seq
def head(sequence):
    return next(_itertools.islice(sequence, 1))


@Seq
def takeWhile(sequence, function):
    return _itertools.takewhile(function, sequence)


@Seq
def find(sequence, function):
    return next(_itertools.ifilter(function, sequence))


@Seq
def rev(sequence):
    return reversed(list(sequence))


@Seq
def zip(sequence1, sequence2):
    return _itertools.izip(sequence1, sequence2)


# class Seq:
#     def __init__(self, value = None):
#         self.value = value
#
#     def sum(self):
#         return sum(self.value)
#
#     def product(self):
#         return reduce(lambda a,b: a*b, self.value)
#
#     def fold(self, function, initial=None):
#         import functools
#         return functools.reduce(function, self.value, initial)
#
#     def head(self):
#         return list(self.take(1).value)[0]
#
#     def max(self):
#         return max(self.value)
#
#     def maxBy(self, f):
#         return max(self.value, key=f)
#
#     def find(self, f):
#         return next(self.filter(f).value, None)
#
#     def findIndex(self,f):
#         return Seq(enumerate(self.value)).find(lambda x: f(x[1]))[0]
#
#     def maxIndex(self):
#         import operator
#         max_index, _ = max(enumerate(self.value), key=operator.itemgetter(1))
#         return max_index
#
#     def filter(self, f):
#         from itertools import ifilter
#         self.value = ifilter(f, self.value)
#         return self
#
#     def map(self, f):
#         from itertools import imap
#         self.value = imap(f, self.value)
#         return self
#
#     def zip(self, other):
#         from itertools import izip
#         self.value = izip(self.value, other.value)
#         return self
#
#
#     def reverse(self):
#         return Seq(reversed(list(self.value)))
#
#
#     def count(self):
#         from itertools import groupby
#         self.value = ((item, len(list(group)))
#                       for item, group in groupby(sorted(self.value)))
#         return self
#
#     def flatten(self):
#         from itertools import chain
#         "Flatten one level of nesting"
#         self.value = chain.from_iterable(self.map(lambda x: x.value).value)
#         return self
#
#     def window(self, n=2):
#         self.value = _window(self.value, n)
#         return self
#
#     def takeWhile(self, f):
#         from itertools import takewhile
#         self.value = takewhile(f, self.value)
#         return self
#
#     def take(self, n):
#         from itertools import islice
#         "Return first n items of the iterable as a list"
#         self.value = islice(self.value, n)
#         return self
#
#     def toList(self):
#         return list(self.value)
#
#     @staticmethod
#     def range(n):
#         return Seq(xrange(n))
#
#     @staticmethod
#     def unfold(f, x0):
#         def seq(x):
#             while x is not None:
#                 w, x = f(x)
#                 yield w
#         return Seq(seq(x0))
