#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_skin
----------------------------------

Tests for `skin` module.
"""

import unittest

from wikipediabase import skin

class TestSkin(unittest.TestCase):

    def setUp(self):
        self.skin = skin.Skin()
        self.skin.set("attr", "val")
        self.skin.append("lst", "v1")
        self.skin.append("lst", "v2")

    def test_io(self):
        self.assertEqual(self.skin.get("attr"), "val")
        self.assertIn("v1", self.skin.get("lst"))


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
