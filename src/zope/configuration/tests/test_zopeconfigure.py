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
"""Test zope.configuration.xmlconfig.
"""
import unittest


class ZopeConfigureTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ZopeConfigure
        return ZopeConfigure

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ZopeConfigureTests),
    ))
