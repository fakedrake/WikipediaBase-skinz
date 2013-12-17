#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_api
----------------------------------

Tests for `api` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase.api import wb_advertise_fn, wb_get_fn, wb_advertise

@wb_advertise_fn
def func():
    pass

class Foo(object):
    @wb_advertise
    def _member():
        pass

    @wb_advertise("member")
    def not_member():
        pass

class TestApi(unittest.TestCase):

    def setUp(self):
        pass

    def test_advertisement(self):
        # Note that to make an unbound method into a function i need
        # to turn it into a staticmethod. But I have no idea what is a
        # class method and what is a function in advance. One way is
        # to have two decorators...
        self.assertIs(wb_get_fn("_member"), Foo._member.__func__)
        self.assertIs(wb_get_fn("member"), Foo.not_member.__func__)
        self.assertIs(wb_get_fn("func"), func)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
