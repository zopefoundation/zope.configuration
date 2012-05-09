##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for for zope.configuration.docutils
"""
import unittest


class Test_wrap(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.docutils import wrap
        return wrap(*args, **kw)

    def test_empty(self):
        self.assertEqual(self._callFUT(''), '\n\n')

    def test_only_whitespace(self):
        self.assertEqual(self._callFUT(' \t\n\r'), '\n\n')

    def test_single_paragraphs(self):
        self.assertEqual(
                self._callFUT('abcde fghij klmno pqrst uvwxy', 10, 3),
                '   abcde\n   fghij\n   klmno\n   pqrst\n   uvwxy\n\n')

    def test_multiple_paragraphs(self):
        self.assertEqual(
                self._callFUT('abcde fghij klmno\n\npqrst uvwxy', 10, 3),
                '   abcde\n   fghij\n   klmno\n\n   pqrst\n   uvwxy\n\n')


class Test_makeDocStructures(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.docutils import makeDocStructures
        return makeDocStructures(*args, **kw)

    # TODO:  coverage


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test_wrap),
        unittest.makeSuite(Test_makeDocStructures),
    ))
