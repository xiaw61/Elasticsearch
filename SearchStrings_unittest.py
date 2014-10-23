__author__ = 'xiaw'

import unittest

from SearchStrings import *


class SearchStringsTest(unittest.TestCase):
    def test(self):
        search = SearchStrings()

        # case 0
        # No query string
        self.assertEqual(search.main([]), "")

        #case 1
        # Result has less than 10
        reference1 = "1th file:news/58057\n"
        self.assertEqual(search.main(["rousseaua@immunex.com"]), reference1)

        #case 2
        reference2 = """1th file:news/4/4f1
2th file:news/4/4f3
3th file:news/4/4f2
4th file:news/4/4f4
5th file:news/2/2f2
6th file:news/3/3f1
7th file:news/3/3f3
8th file:news/3/3f2
9th file:news/58057
10th file:news/2/2f
"""
        self.assertEqual(search.main(["or", "is"]), reference2)


if __name__ == '__main__':
    unittest.main()