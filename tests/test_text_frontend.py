#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_text_frontend
----------------------------------

Tests for `text_frontend` module.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wikipediabase import text_frontend

import wikipediabase.api as api

@api.advertise()
def mysplit(s):
    return s.split()

class TestTextFrontend(unittest.TestCase):

    def setUp(self):
        pass

    def test_basics(self):
        self.assertEqual(api.freecall("frontend", "(mysplit \"1 2 3\")"),
                         ['1', '2', '3'])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
