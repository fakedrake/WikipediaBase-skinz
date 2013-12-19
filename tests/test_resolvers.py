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

    def test_yomama(self):
        self.assertEqual(api.freecall("attribute-resolver", "be-fat", "yomama"), 'yomama be-fat')

    def test_swearwords(self):
        # Resolution of static attributes will fail on attribute "on"
        # (only "yomama" static attribute is available) and will
        # fallback to resolving using 'nearby_swearwords'
        self.assertEqual(api.freecall("attribute-resolver", "shit is on me shoes", "on"), ['shit'])

    def test_extended_swearwords(self):
        # This should match the old swear words and some extra
        api.append('swearwords', "pedantic")
        api.set('nearby-word-distance', 5)
        self.assertEqual(api.freecall("attribute-resolver", "fuck you sir, you are shallow and pedantic", "are"), ['fuck', 'pedantic'])


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
