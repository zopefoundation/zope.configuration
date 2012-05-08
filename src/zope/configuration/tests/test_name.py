##############################################################################
#
# Copyright (c) 20!2 Zope Foundation and Contributors.
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
"""Test zope.configuration.name
"""
import unittest


class Test_resolve(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.name import resolve
        return resolve(*args, **kw)


class Test_getNormalizedName(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.name import getNormalizedName
        return getNormalizedName(*args, **kw)


class Test_path(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.name import path
        return path(*args, **kw)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(Test_resolve),
        unittest.makeSuite(Test_resolve),
        unittest.makeSuite(Test_path),
    ))
