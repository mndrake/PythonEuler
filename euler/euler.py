import numpy as np
import operator
from sys import setrecursionlimit
setrecursionlimit(4000)


# utility methods ------------------------------------

def memoize(f):
  class memodict(dict):
      __slots__ = ()
      def __missing__(self, key):
          self[key] = ret = f(key)
          return ret
  return memodict().__getitem__


def timer(f):
    from timeit import default_timer
    start = default_timer()
    result = f()
    end = default_timer()
    print 'result:', result, '(%.2fs)' % (end - start)


def readlines(file):
    return open(file).read().splitlines()

fst = operator.itemgetter(0)
snd = operator.itemgetter(1)

# number theory methods ---------------------------------------

# prime list cache
_primes = [2]


def _grow_primes():
    p0 = _primes[len(_primes) - 1] + 1
    b = np.ones(p0, dtype=bool)
    for di in _primes:
        i0 = p0 / di * di
        if i0 < p0:
            b[i0 + di - p0::di] = False
        else:
            b[i0 - p0::di] = False
    _primes.extend(np.where(b)[0] + p0)


def primes():
    i = 0
    while True:
        if i >= len(_primes): _grow_primes()
        yield _primes[i]
        i += 1


def prime(n):
    while n >= len(_primes): _grow_primes()
    return _primes[n]


def is_prime(n):
    if n < 1:
        return False
    ps = primes()
    p = ps.next()
    while p * p <= n:
        if n % p == 0:
            return False
        p = ps.next()
    return True


def GCD(a,b):
    """https://reference.wolfram.com/language/ref/GCD.html"""
    while b:
        a, b = b, a%b
    return a


def LCM(a,b):
    """https://reference.wolfram.com/language/ref/LCM.html"""
    return a / GCD(a,b) * b


def FactorInteger(n):
    """https://reference.wolfram.com/language/ref/FactorInteger.html"""
    from itertools import groupby
    factors = []
    ps = primes()
    m = n
    p = ps.next()
    while p*p <= m:
        if m%p==0:
            m /= p
            factors.append(p)
        else:
            p = ps.next()
    factors.append(m)
    return list((item, len(list(group)))
                for item, group
                in groupby(sorted(factors)))


def DivisorSigma(n):
    """https://reference.wolfram.com/language/ref/DivisorSigma.html"""
    import operator
    return reduce(operator.mul,
                  [(x[1] + 1) for x in FactorInteger(n)],
                  1)

# lazy lists ---------------------------------------------------


# def _window(seq, n=2):
#     from itertools import islice
#
#     "Returns a sliding window (of width n) over data from the iterable"
#     "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
#     it = iter(seq)
#     result = tuple(islice(it, n))
#     if len(result) == n:
#         yield result
#     for elem in it:
#         result = result[1:] + (elem,)
#         yield result


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
