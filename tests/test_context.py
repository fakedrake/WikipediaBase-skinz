#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_context
----------------------------------

Tests for `context` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase.context import wbregister_named, wbcall

@wbregister_named("addone")
def addone(x):
    return x+1

class TestContext(unittest.TestCase):

    def setUp(self):
        pass

    def test_regdec(self):
        self.assertEqual(wbcall("addone", 1), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
