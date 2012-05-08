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
"""Test zope.configuration.fields.
"""
import unittest


class PythonIdentifierTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import PythonIdentifier
        return PythonIdentifier
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class GlobalObjectTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import GlobalObject
        return GlobalObject
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class GlobalIdentifierTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import GlobalIdentifier
        return GlobalIdentifier
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class TokensTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import Tokens
        return Tokens
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class PathTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import Path
        return Path
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class BoolTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import Bool
        return Bool
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class MessageIDTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import MessageID
        return MessageID
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)



def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PythonIdentifierTests),
        unittest.makeSuite(GlobalObjectTests),
        unittest.makeSuite(GlobalIdentifierTests),
        unittest.makeSuite(TokensTests),
        unittest.makeSuite(PathTests),
        unittest.makeSuite(BoolTests),
        unittest.makeSuite(MessageIDTests),
        ))
