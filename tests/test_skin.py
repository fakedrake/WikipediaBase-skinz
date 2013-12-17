#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_skin
----------------------------------

Tests for `skin` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase import skin

JSON_CODE = """{"a": 3}
"""


class TestSkin(unittest.TestCase):

    def setUp(self):
        self.skin = skin.Skin()
        self.skin.set("attr", "val")
        self.skin.append("lst", "v1")
        self.skin.append("lst", "v2")

    def test_io(self):
        self.assertEqual(self.skin.get("attr"), "val")
        self.assertEqual(["v2", "v1"], self.skin.get("lst"))

    def test_parent(self):
        new_skin = skin.Skin(parent=self.skin)
        new_skin["new_attr"] = "new_val"

        self.assertEqual(new_skin.get("attr"), "val")
        self.assertEqual(new_skin.get("new_attr"), "new_val")
        self.assertEqual(self.skin.get("new_attr"), None)

    def test_json(self):
        self.skin.set_config(skin.JsonSkinConfig(string=JSON_CODE))
        self.assertEqual(self.skin["a"], 3)

    def test_dump(self):
        self.assertEqual(self.skin.dump(),
                         '{"lst": ["v2", "v1"], "attr": "val"}')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
