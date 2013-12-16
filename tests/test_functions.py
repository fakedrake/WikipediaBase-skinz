#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_functions
----------------------------------

Tests for `functions` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase import functions

def addone(x):
    return x+1

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.fns = functions.FunctionSkin()
        self.fns.add_function(addone)

    def test_addition(self):
        self.assertEqual(self.fns["addone"], ('tests.test_functions', 'addone'))

    def test_calling(self):
        self.assertEqual(self.fns.call("addone", 1), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
