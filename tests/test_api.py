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

import wikipediabase.api as api

JSON_DUMP = '{"test-frontend": ["tests.test_api", [], "frontend"], "default_kwargs": {"domain": "functions", "mapping": true, "append": null}, "functions": {"member": ["tests.test_api", ["Foo"], "not_member"], "mysplit": ["tests.test_text_frontend", [], "mysplit"], "_member": ["tests.test_api", ["Foo"], "_member"], "func": ["tests.test_api", [], "func"]}, "frontend": ["wikipediabase.text_frontend", [], "text_frontend"]}'

# Maybe defining domain should imply append but I will consider it a
# design descision to leave it like this.
@api.advertise(domain="test-frontend", append=False)
def frontend(inp):
    return inp.split()

@api.advertise()
def func():
    pass

class Foo(api.Advertisable):
    @api.advertise()
    def _member():
        pass

    # advertise will not deal with staticmethod type fns very well.
    @api.advertise(name="member")
    def not_member():
        return 2

class TestApi(unittest.TestCase):

    def setUp(self):
        pass

    def test_advertisement(self):
        # Note that to make an unbound method into a function i need
        # to turn it into a staticmethod. But I have no idea what is a
        # class method and what is a function in advance. One way is
        # to have two decorators...
        self.assertIs(api.get_fn("_member"), Foo._member)
        # Notice how static methods are translated into proper
        # functions and not unbound.
        self.assertIs(api.get_fn("member"), Foo.not_member)
        self.assertIs(api.get_fn("func"), func)
        self.assertIs(api.get("test-frontend"), frontend)

    def test_calling(self):
        self.assertEqual(api.call("member"), 2)
        self.assertEqual(api.freecall("test-frontend", "a string to split"),
                         ['a', 'string', 'to', 'split'])

    def test_dumping(self):
         self.assertEqual(api.jsondump(),JSON_DUMP)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
