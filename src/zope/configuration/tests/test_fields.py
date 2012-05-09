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


class _ConformsToIFromUnicode(object):

    def test_class_conforms_to_IFromUnicode(self):
        from zope.interface.verify import verifyClass
        from zope.schema.interfaces import IFromUnicode
        verifyClass(IFromUnicode, self._getTargetClass())

    def test_instance_conforms_to_IFromUnicode(self):
        from zope.interface.verify import verifyObject
        from zope.schema.interfaces import IFromUnicode
        verifyObject(IFromUnicode, self._makeOne())


class PythonIdentifierTests(unittest.TestCase, _ConformsToIFromUnicode):

    def _getTargetClass(self):
        from zope.configuration.fields import PythonIdentifier
        return PythonIdentifier
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_fromUnicode_empty(self):
        pi = self._makeOne()
        self.assertEqual(pi.fromUnicode(''), '')

    def test_fromUnicode_normal(self):
        pi = self._makeOne()
        self.assertEqual(pi.fromUnicode('normal'), 'normal')

    def test_fromUnicode_strips_ws(self):
        pi = self._makeOne()
        self.assertEqual(pi.fromUnicode('   '), '')
        self.assertEqual(pi.fromUnicode(' normal  '), 'normal')

    def test__validate_miss(self):
        from zope.schema import ValidationError
        from zope.configuration._compat import u
        pi = self._makeOne()
        self.assertRaises(ValidationError,
                          pi._validate, u('not-an-identifier'))

    def test__validate_hit(self):
        from zope.configuration._compat import u
        pi = self._makeOne()
        pi._validate(u('is_an_identifier'))


class GlobalObjectTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import GlobalObject
        return GlobalObject
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test__validate_wo_value_type(self):
        from zope.configuration._compat import u
        from zope.configuration._compat import b
        go = self._makeOne(value_type=None)
        for value in [0, 0.0, (), [], set(), frozenset(), u(''), b('')]:
            go._validate(value) #noraise

    def test__validate_w_value_type(self):
        from zope.schema import Text
        from zope.schema.interfaces import WrongType
        from zope.configuration._compat import u
        from zope.configuration._compat import b
        go = self._makeOne(value_type=Text())
        go.validate(u(''))
        for value in [0, 0.0, (), [], set(), frozenset(), b('')]:
            self.assertRaises(WrongType, go._validate, value)

    def test_fromUnicode_w_star_and_extra_ws(self):
        go = self._makeOne()
        self.assertEqual(go.fromUnicode(' * '), None)

    def test_fromUnicode_w_resolve_fails(self):
        from zope.schema import ValidationError
        from zope.configuration.config import ConfigurationError
        class Context(object):
            def resolve(self, name):
                self._resolved = name
                raise ConfigurationError()
        go = self._makeOne()
        context = Context()
        bound = go.bind(context)
        self.assertRaises(ValidationError, bound.fromUnicode, 'tried')
        self.assertEqual(context._resolved, 'tried')

    def test_fromUnicode_w_resolve_success(self):
        _target = object()
        class Context(object):
            def resolve(self, name):
                self._resolved = name
                return _target
        go = self._makeOne()
        context = Context()
        bound = go.bind(context)
        found = bound.fromUnicode('tried')
        self.assertTrue(found is _target)
        self.assertEqual(context._resolved, 'tried')

    def test_fromUnicode_w_resolve_but_validation_fails(self):
        from zope.schema import Text
        from zope.schema import ValidationError
        _target = object()
        class Context(object):
            def resolve(self, name):
                self._resolved = name
                return _target
        go = self._makeOne(value_type=Text())
        context = Context()
        bound = go.bind(context)
        self.assertRaises(ValidationError, bound.fromUnicode, 'tried')
        self.assertEqual(context._resolved, 'tried')


class GlobalIdentifierTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import GlobalIdentifier
        return GlobalIdentifier
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class TokensTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import Tokens
        return Tokens
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class PathTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import Path
        return Path
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class BoolTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import Bool
        return Bool
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class MessageIDTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.fields import MessageID
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
