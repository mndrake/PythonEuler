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

def init(n, function):
    i = 0
    while i < n:
        yield function(i)
        i += 1

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
        return _itertools.imap(function, sequence)


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


@Seq
def flatten(sequence):
    return _itertools.chain.from_iterable(_itertools.imap(lambda x: x, sequence))


@Seq
def length(sequence):
    count = 0
    for x in sequence:
        count += 1
    return count

#     def count(self):
#         from itertools import groupby
#         self.value = ((item, len(list(group)))
#                       for item, group in groupby(sorted(self.value)))
#         return self
#


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
#
#
# class Seq:
#     """
#     Represent a Pipeable Element :
#     Described as :
#     first = Seq(lambda iterable: next(iter(iterable)))
#     and used as :
#     print [1, 2, 3] >> first
#     printing 1
#
#     Or represent a Pipeable Function :
#     It's a function returning a Seq
#     Described as :
#     select = Seq(lambda iterable, pred: (pred(x) for x in iterable))
#     and used as :
#     print [1, 2, 3] >> select(lambda x: x * 2)
#     # 2, 4, 6
#     """
#     def __init__(self, function):
#         self.function = function
#
#     def __rrshift__(self, other):
#         return self.function(other)
#
#     def __call__(self, *args, **kwargs):
#         return Seq(lambda x: self.function(x, *args, **kwargs))
#
# @Seq
# def take(iterable, qte):
#     "Yield qte of elements in the given iterable."
#     for item in iterable:
#         if qte > 0:
#             qte -= 1
#             yield item
#         else:
#             return
#
# @Seq
# def tail(iterable, qte):
#     "Yield qte of elements in the given iterable."
#     out = []
#     for item in iterable:
#         out.append(item)
#         if len(out) > qte:
#             out.pop(0)
#     return out
#
# @Seq
# def skip(iterable, qte):
#     "Skip qte elements in the given iterable, then yield others."
#     for item in iterable:
#         if qte == 0:
#             yield item
#         else:
#             qte -= 1
#
# @Seq
# def all(iterable, pred):
#     "Returns True if ALL elements in the given iterable are true for the given pred function"
#     return builtins.all(pred(x) for x in iterable)
#
# @Seq
# def any(iterable, pred):
#     "Returns True if ANY element in the given iterable is True for the given pred function"
#     return builtins.any(pred(x) for x in iterable)
#
# @Seq
# def average(iterable):
#     """
#     Build the average for the given iterable, starting with 0.0 as seed
#     Will try a division by 0 if the iterable is empty...
#     """
#     total = 0.0
#     qte = 0
#     for x in iterable:
#         total += x
#         qte += 1
#     return total / qte
#
# @Seq
# def count(iterable):
#     "Count the size of the given iterable, walking thrue it."
#     count = 0
#     for x in iterable:
#         count += 1
#     return count
#
# @Seq
# def max(iterable, **kwargs):
#     return builtins.max(iterable, **kwargs)
#
# @Seq
# def min(iterable, **kwargs):
#     return builtins.min(iterable, **kwargs)
#
# @Seq
# def as_dict(iterable):
#     return dict(iterable)
#
# @Seq
# def permutations(iterable, r=None):
#     # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
#     # permutations(range(3)) --> 012 021 102 120 201 210
#     for x in itertools.permutations(iterable, r):
#         yield x
#
# @Seq
# def netcat(to_send, host, port):
#     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#         s.connect((host, port))
#         for data in to_send >> traverse:
#             s.send(data)
#         while 1:
#             data = s.recv(4096)
#             if not data: break
#             yield data
#
# @Seq
# def netwrite(to_send, host, port):
#     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#         s.connect((host, port))
#         for data in to_send >> traverse:
#             s.send(data)
#
# @Seq
# def traverse(args):
#     for arg in args:
#         try:
#             if isinstance(arg, str):
#                 yield arg
#             else:
#                 for i in arg >> traverse:
#                     yield i
#         except TypeError:
#             # not iterable --- output leaf
#             yield arg
#
# @Seq
# def concat(iterable, separator=", "):
#     return separator.join(map(str,iterable))
#
# @Seq
# def as_list(iterable):
#     return list(iterable)
#
# @Seq
# def as_tuple(iterable):
#     return tuple(iterable)
#
# @Seq
# def stdout(x):
#     sys.stdout.write(str(x))
#
# @Seq
# def lineout(x):
#     sys.stdout.write(str(x) + "\n")
#
# @Seq
# def tee(iterable):
#     for item in iterable:
#         sys.stdout.write(str(item) + "\n")
#         yield item
#
# @Seq
# def add(x):
#     return sum(x)
#
# @Seq
# def first(iterable):
#     return next(iter(iterable))
#
# @Seq
# def chain(iterable):
#     return itertools.chain(*iterable)
#
# @Seq
# def select(iterable, selector):
#     return (selector(x) for x in iterable)
#
# @Seq
# def where(iterable, predicate):
#     return (x for x in iterable if (predicate(x)))
#
# @Seq
# def take_while(iterable, predicate):
#     return itertools.takewhile(predicate, iterable)
#
# @Seq
# def skip_while(iterable, predicate):
#     return itertools.dropwhile(predicate, iterable)
#
# @Seq
# def aggregate(iterable, function, **kwargs):
#     if 'initializer' in kwargs:
#         return reduce(function, iterable, kwargs['initializer'])
#     else:
#         return reduce(function, iterable)
# @Seq
# def groupby(iterable, keyfunc):
#     return itertools.groupby(sorted(iterable, key = keyfunc), keyfunc)
#
# @Seq
# def sort(iterable, **kwargs):
#     return sorted(iterable, **kwargs)
#
# @Seq
# def reverse(iterable):
#     return reversed(iterable)
#
# @Seq
# def passed(x):
#     pass
#
# @Seq
# def index(iterable, value, start=0, stop=None):
#     return iterable.index(value, start, stop or len(iterable))
#
# @Seq
# def strip(iterable, chars=None):
#     return iterable.strip(chars)
#
# @Seq
# def rstrip(iterable, chars=None):
#     return iterable.rstrip(chars)
#
# @Seq
# def lstrip(iterable, chars=None):
#     return iterable.lstrip(chars)
#
# @Seq
# def run_with(iterable, func):
#     return  func(**iterable) if isinstance(iterable, dict) else \
#             func( *iterable) if hasattr(iterable,'__iter__') else \
#             func(  iterable)
#
# @Seq
# def t(iterable, y):
#     if hasattr(iterable,'__iter__') and not isinstance(iterable, str):
#         return iterable + type(iterable)([y])
#     else:
#         return [iterable, y]
#
# @Seq
# def to_type(x, t):
#     return t(x)
#
# chain_with = Seq(itertools.chain)
# islice = Seq(itertools.islice)
#
# # Python 2 & 3 compatibility
# if "izip" in dir(itertools):
#     izip = Seq(itertools.izip)
# else:
#     izip = Seq(zip)
#
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()