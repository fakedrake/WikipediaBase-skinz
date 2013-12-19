#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_resolvers
----------------------------------

Tests for `resolvers` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase import resolvers, api

class TestResolvers(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        self.assertEqual(api.freecall("attribute-resolver", "be-fat", "yomama"), 'yomama be-fat')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
