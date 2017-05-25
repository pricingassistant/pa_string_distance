# cython: profile=True

from __future__ import division
from unidecode import unidecode
import re2
from itertools import combinations

cdef double jaro_winkler_ratio(s1, s2):
  u1 = unicode(s1)
  u2 = unicode(s2)
  return jaro_winkler(u1, len(u1), u2, len(u2), 0)

RE_SPLIT = re2.compile(r"(?:[^\w]|[_])+")
RE_ISNUM = re2.compile(r"[0-9]")


cdef float norm(flt, from1, to1, from2, to2):
  return ((flt - from1) / (to1 - from1)) * (to2 - from2) + from2

# Resampled because we don't care about really different strings
def jaro(s1, s2):
  j = jaro_winkler_ratio(s1, s2)

  if j < 0.75:
    return 0
  elif j < 0.85:
    return norm(j, 0, 0.85, 0, 0.01)
  else:
    return norm(j, 0.85, 1, 0.01, 1)

cdef tokenize(s):
  s = s.lower()
  if type(s) == unicode:
    s = unidecode(s)
  return [x for x in RE_SPLIT.split(s) if x]

cdef float w(tokens):
  """ Returns the weight of a list of tokens """
  cdef float s = 0.0
  for t in tokens:
    s += len(t)
  return s

cdef reassemble(joiner, tokens, whitelist):
  return joiner.join([t for t in tokens if t in whitelist])

def pa_string_distance(str1, str2):

  if not str1 or not str2:
    return 1.0

  tokens1 = tokenize(str1)
  tokens2 = tokenize(str2)

  # print tokens1, tokens2

  if len(tokens1) == 0 or len(tokens2) == 0:
    return 1.0

  tokens1_set = set(tokens1)
  tokens2_set = set(tokens2)

  weight1 = w(tokens1_set)
  weight2 = w(tokens2_set)

  max_distance = weight1 + weight2
  cdef float distance = 0.0

  # intersection = tokens1_set.intersection(tokens2_set)

  diff1 = set()
  diff1_num = set()

  diff2 = set()
  diff2_num = set()

  for t in tokens1_set.difference(tokens2_set):
    if RE_ISNUM.search(t):
      diff1_num.add(t)
    else:
      diff1.add(t)

  for t in tokens2_set.difference(tokens1_set):
    if RE_ISNUM.search(t):
      diff2_num.add(t)
    else:
      diff2.add(t)

  # print diff1, diff1_num
  # print diff2, diff2_num

  cdef float diff1_weight = w(diff1)
  cdef float diff2_weight = w(diff2)
  cdef float diff1_num_weight = w(diff1_num)
  cdef float diff2_num_weight = w(diff2_num)

  distance += diff1_num_weight + diff2_num_weight

  if len(diff1) == 0 and len(diff2) == 0:
    return distance / max_distance

  # By now, we have eliminated all the simple cases.
  # Compare the remainders with a few different methods and pick the lowest distance.

  # 1: smallest jaro distance in all the tokens of the other string
  jaro1 = sum([min([1 - jaro(t1, t2) for t2 in tokens2_set]) * len(t1) for t1 in diff1])
  jaro2 = sum([min([1 - jaro(t1, t2) for t1 in tokens1_set]) * len(t2) for t2 in diff2])

  distance_crossproduct = (distance + jaro1 + jaro2)

  # 2: original order diffs
  original1 = reassemble(" ", tokens1, diff1)
  original2 = reassemble(" ", tokens2, diff2)

  cdef float weight = (1 - jaro(original1, original2)) * (diff1_weight + diff2_weight)
  cdef float distance_originalorder = (distance + weight)

  # 2: original order diffs, with numerics
  originalnum1 = reassemble("", tokens1, diff1.union(diff1_num))
  originalnum2 = reassemble("", tokens2, diff2.union(diff2_num))

  cdef float coef = (diff1_weight + diff2_weight + diff1_num_weight + diff2_num_weight)
  weight = (1 - jaro(originalnum1, originalnum2)) * coef
  cdef float distance_originalorderwithnum = min(weight + 0.01, coef)  # Add an additional fixed distance here to differentiate cases.

  return min([distance_crossproduct, distance_originalorder, distance_originalorderwithnum]) / max_distance
