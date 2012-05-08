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

    # TODO:  coverage


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
