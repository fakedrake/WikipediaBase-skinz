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

from wikipediabase.functions import FunctionSkin
from wikipediabase.context import Context

def addone(x):
    return x+1

class TestContext(unittest.TestCase):

    def setUp(self):
        self.s = Context._skin
        Context._skin = None

    def test_skin_generation(self):
        self.sn = len(list(Context.skins()))
        self.assertTrue(isinstance(Context.get_skin(function=True), FunctionSkin))
        self.assertTrue(isinstance(Context._skin, FunctionSkin))
        self.assertEqual(len(list(Context.skins())), self.sn+1)


    def tearDown(self):
        Context._skin = self.s

if __name__ == '__main__':
    unittest.main()
