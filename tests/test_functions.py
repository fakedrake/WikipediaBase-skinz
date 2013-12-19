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

from wikipediabase import functions, skin

def addone(x):
    return x+1

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.fns = functions.FunctionSkin()
        self.fns.set('addone', addone)

    def test_serialfn(self):
        self.assertEqual(tuple(functions.SerialFunction(fn=addone)), ('tests.test_functions', [], 'addone'))

    def test_addition(self):
        self.assertEqual(tuple(skin.Skin.get(self.fns, "addone")), ('tests.test_functions', [], 'addone'))
        self.assertIs(self.fns['addone'], addone)

    def test_calling(self):
        self.assertEqual(self.fns.get("addone")(1), 2)

    def test_dump(self):
        self.assertEqual(self.fns.dump(), '{"addone": ["tests.test_functions", [], "addone"]}')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
