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

    def test_top_level_module(self):
        import os
        self.assertTrue(self._callFUT('os') is os)

    def test_nested_module(self):
        import os.path
        self.assertTrue(self._callFUT('os.path') is os.path)

    def test_function_in_module(self):
        import os.path
        self.assertTrue(self._callFUT('os.path.join') is os.path.join)

    def test_importable_but_not_attr_of_parent(self):
        import sys
        import zope.configuration.tests as zct
        self.assertFalse('notyet' in zct.__dict__)
        mod = self._callFUT('zope.configuration.tests.notyet')
        self.assertTrue(mod is zct.notyet)
        del zct.notyet
        del sys.modules['zope.configuration.tests.notyet']

    def test_function_in_module_relative(self):
        import os.path
        self.assertTrue(self._callFUT('.join', 'os.path') is os.path.join)

    def test_class_in_module(self):
        from zope.configuration.tests.directives import Complex
        self.assertTrue(
            self._callFUT('zope.configuration.tests.directives.Complex')
                    is Complex)

    def test_class_w_same_name_as_module(self):
        from zope.configuration.tests.samplepackage.NamedForClass \
            import NamedForClass
        self.assertTrue(
            self._callFUT(
                'zope.configuration.tests.samplepackage.NamedForClass+')
                    is NamedForClass)
        self.assertTrue(
            self._callFUT(
                'zope.configuration.tests.samplepackage.NamedForClass.')
                    is NamedForClass)

class Test_getNormalizedName(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.name import getNormalizedName
        return getNormalizedName(*args, **kw)

    def test_no_dots(self):
        self.assertEqual(self._callFUT('os', None), 'os')

    def test_one_dot(self):
        self.assertEqual(self._callFUT('os.path', None), 'os.path')

    def test_two_dots(self):
        self.assertEqual(self._callFUT('os.path.join', None), 'os.path.join')

    def test_relative(self):
        self.assertEqual(self._callFUT('.join', 'os.path'), 'os.path.join')

    def test_repeat_plus(self):
        self.assertEqual(
            self._callFUT('zope.configuration.tests.NamedForClass+', None),
            'zope.configuration.tests.NamedForClass+')

    def test_repeat_dot(self):
        self.assertEqual(
            self._callFUT('zope.configuration.tests.NamedForClass.', None),
            'zope.configuration.tests.NamedForClass+')

    def test_repeat_inferred(self):
        self.assertEqual(
            self._callFUT(
                'zope.configuration.tests.NamedForClass.NamedForClass', None),
            'zope.configuration.tests.NamedForClass+')


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
