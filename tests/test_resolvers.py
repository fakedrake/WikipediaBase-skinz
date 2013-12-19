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

import re


@api.advertise(domain="static-attribute-resolvers", name="wordcount")
def word_count(article):
    return len(resolvers._wordlist(article))

# Attribute resolvers is just a list of things
@api.advertise(domain="attribute-resolvers", mapping=False)
def wordoccurances(fetcher, article, attribute):
    m = re.match("count(\\w+)", attribute)

    if m:
        return len([w for w in resolvers._wordlist(article) if w == m.group(1).lower()])


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

    def test_extended_statics(self):
        # New static attribute resolvers were defined here.
        self.assertEqual(api.freecall("attribute-resolver", "fuck you sir, you are shallow and pedantic", "wordcount"), 8)

    def test_extended_generics(self):
        # New gereic resolvers were defined.
        self.assertEqual(api.freecall("attribute-resolver", "fuck you sir, you are shallow and pedantic", "countyou"), 2)

        # Here you see how the newly defined resolvers override the
        # old ones. (the old one would have found the nearest
        # swearwords)
        self.assertEqual(api.freecall("attribute-resolver", "fuck you sir, you are shallow and pedantic countyou", "countyou"), 2)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
