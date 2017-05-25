from pa_string_distance import pa_string_distance
import timeit
import pytest


def string_compare(s1, s2):
    return {
        "ratio": 1 - pa_string_distance(s1, s2)
    }


def test_string_compare():

  # Change this for performance tests
  for _ in range(10000):

    assert 1 == string_compare("boite de trucs", "boite de trucs")["ratio"]

    # repeats
    assert 1 == string_compare("boite de trucs trucs", "boite de trucs")["ratio"]
    assert 1 == string_compare("boite de trucs trucs", "boite de trucs boite")["ratio"]

    # punctuation
    assert 1 == string_compare("boite de trucs trucs.", " Boite de trucs boite, boite!")["ratio"]
    assert 1 == string_compare("Finish line", "Finish-line")["ratio"]

    partial_match = string_compare("super boite de trucs", "boite de trucs")["ratio"]
    assert partial_match < 1

    partial_double_match = string_compare("super boite de trucs", "mega boite de trucs")["ratio"]
    assert partial_double_match < partial_match

    partial_double_match_larger = string_compare("vraiment super boite de trucs", "mega boite de trucs")["ratio"]
    partial_double_match_larger < partial_double_match

    mismatch = string_compare("vraiment super", "mega bien")["ratio"]

    assert mismatch < partial_double_match_larger
    assert mismatch < 0.1

    zero = string_compare("e", "a")["ratio"]
    assert zero == 0

    # empty strings
    assert 0 == string_compare("", "")["ratio"]
    assert 0 == string_compare(" ", "")["ratio"]
    assert 0 == string_compare(", ", "")["ratio"]
    assert 0 == string_compare(", ", " ")["ratio"]
    assert 0 == string_compare(" ", " ")["ratio"]
    assert 0 == string_compare(",", " ")["ratio"]
    assert 0 == string_compare(" , ", "    ,  ,,,")["ratio"]

    assert 0 == string_compare("", "a")["ratio"]
    assert 0 == string_compare(",", "a")["ratio"]
    assert 0 == string_compare(", ", "a, ")["ratio"]
    assert 0 == string_compare(" ", "R22")["ratio"]

    # Numerical mis-spellings are not allowed
    assert 0 == string_compare("R19", "R20")["ratio"]
    assert 0 == string_compare("405L", "406L")["ratio"]
    assert 0 == string_compare("Peugeot", "R22")["ratio"]
    assert 0 == string_compare("Citroen", "R22")["ratio"]
    assert 0 == string_compare("PeugeotCitroen", "R22")["ratio"]

    # Really different strings shouldn't match at all either
    assert 0.01 > string_compare("renault", "peugeot")["ratio"]
    assert 0 == string_compare("Cabriolet", "R")["ratio"]

    # Somewhat close strings
    assert 0 < string_compare("peugot", "peugeot")["ratio"] < string_compare("xxxxxxxpeugot", "xxxxxxxpeugeot")["ratio"]

    # Grouping
    assert 0 < string_compare("PG 38", "PG38")["ratio"]
    assert string_compare("PG 38", "PG38")["ratio"] > string_compare("PG 38", "PG 39")["ratio"]

    assert 0 < string_compare("PG38", "PG-38")["ratio"]
    assert string_compare("PG38", "PG-38")["ratio"] > string_compare("PG38", "PG38 Other")["ratio"]

    assert 0 < string_compare("PG-38", "PG38 Other")["ratio"]
    assert string_compare("PG-38", "PG38 Other")["ratio"] < string_compare("PG38", "PG38 Other")["ratio"]

    assert 0 < string_compare("R20 Cabriolet", "R-20")["ratio"]
    assert string_compare("R20 Cabriolet", "R-20")["ratio"] < string_compare("R20 Cabriolet", "R20")["ratio"]

    assert 0 < string_compare("Finish line", "Finishline")["ratio"]
    assert 1 > string_compare("Finish line", "Finishline")["ratio"]
    assert string_compare("Finish line", "Finishline")["ratio"] > string_compare("Line Finish", "Finishline")["ratio"]
    assert string_compare("Finish line", "Finishline")["ratio"] > string_compare("Finish Leopard", "Finishline")["ratio"]

    # Also work by 3
    assert string_compare("Finish line leftover", "FinishlineLeftover")["ratio"] > string_compare("Finish Leopard Leftover", "FinishlineLeftover")["ratio"]
    assert string_compare("Finish line leftover", "FinishlineLeftover")["ratio"] > 0.8

    # Close string to an existing pair is preferred
    assert string_compare("words word", "words")["ratio"] > string_compare("words wxyz", "words")["ratio"]

    # Special characters
    assert string_compare(u"K\xe4rcher", "KARCHER")["ratio"] > 0.95
