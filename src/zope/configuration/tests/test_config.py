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
"""Test configuration machinery.
"""
import unittest


class ConfigurationContextTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import ConfigurationContext
        return ConfigurationContext
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def assertRaises(self, excClass, callableObj, *args, **kwargs):
        # Morph stdlib version to return the raised exception
        try:
            callableObj(*args, **kwargs)
        except excClass as exc:
            return exc
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException("%s not raised" % excName)

    def test_resolve_trailing_dot_in_resolve(self):
        #Dotted names are no longer allowed to end in dots
        c = self._makeOne()
        self.assertRaises(ValueError, c.resolve, 'zope.')

    def test_resolve_blank(self):
        c = self._makeOne()
        self.assertRaises(ValueError, c.resolve, '   ')

    def test_bad_dotted_last_import(self):
        # Import error caused by a bad last component in the dotted name.
        from zope.configuration.exceptions import ConfigurationError
        c = self._makeOne()
        exc = self.assertRaises(ConfigurationError,
                          c.resolve, 'zope.configuration.tests.nosuch')
        self.assertTrue('ImportError' in str(exc))

    def test_bad_dotted_import(self):
        # Import error caused by a totally wrong dotted name.
        from zope.configuration.exceptions import ConfigurationError
        c = self._makeOne()
        exc = self.assertRaises(ConfigurationError, 
                          c.resolve, 'zope.configuration.nosuch.noreally')
        self.assertTrue('ImportError' in str(exc))

    def test_bad_sub_last_import(self):
        #Import error caused by a bad sub import inside the referenced
        #dotted name. Here we keep the standard traceback.
        import sys
        c = self._makeOne()
        self.assertRaises(ImportError,
                          c.resolve, 'zope.configuration.tests.victim')
        #Cleanup:
        for name in ('zope.configuration.tests.victim',
                     'zope.configuration.tests.bad'):
           if name in sys.modules:
               del sys.modules[name]

    def test_bad_sub_import(self):
        #Import error caused by a bad sub import inside part of the referenced
        #dotted name. Here we keep the standard traceback.
        import sys
        c = self._makeOne()
        self.assertRaises(ImportError, 
                          c.resolve, 'zope.configuration.tests.victim.nosuch')
        #Cleanup:
        for name in ('zope.configuration.tests.victim',
                     'zope.configuration.tests.bad'):
           if name in sys.modules:
               del sys.modules[name]

    def test_path_basepath_absolute(self):
        #Path must always return an absolute path.
        import os
        class stub:
            __file__ = os.path.join('relative', 'path')
        c = self._makeOne()
        c.package = stub()
        self.assertTrue(os.path.isabs(c.path('y/z')))

    def test_path_basepath_uses_dunder_path(self):
        #Determine package path using __path__ if __file__ isn't available.
        # (i.e. namespace package installed with
        #--single-version-externally-managed)
        import os
        class stub:
            __path__ = [os.path.join('relative', 'path')]
        c = self._makeOne()
        c.package = stub()
        os.path.isabs(c.path('y/z'))

    #TODO: coverage


class ConfigurationAdapterRegistryTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import ConfigurationAdapterRegistry
        return ConfigurationAdapterRegistry
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    #TODO: coverage


class ConfigurationMachineTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.config import ConfigurationMachine
        return ConfigurationMachine
    
    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_keyword_handling(self):
        from zope.configuration.config import metans
        from zope.configuration.tests.directives import f
        from zope.configuration._compat import b
        from zope.configuration._compat import u
        machine = self._makeOne()
        ns = "http://www.zope.org/testing"

        #Register some test directives, starting with a grouping directive
        # that sets a package:

        machine((metans, "groupingDirective"),
                 name="package", namespace=ns,
                 schema="zope.configuration.tests.directives.IPackaged",
                 handler="zope.configuration.tests.directives.Packaged",
                )

        # set the package:
        machine.begin((ns, "package"),
                       package="zope.configuration.tests.directives",
                      )

        #Which makes it easier to define the other directives:
        machine((metans, "directive"),
                namespace=ns, name="k",
                schema=".Ik", handler=".k")

        machine((ns, "k"), "yee ha",
                **{"for": u("f"), "class": u("c"), "x": u("x")})

        self.assertEqual(len(machine.actions), 1)
        self.assertEqual(machine.actions[0],
                         {'args': (b('f'), b('c'), b('x')),
                          'callable': f,
                          'discriminator': ('k', b('f')),
                          'includepath': (),
                          'info': 'yee ha',
                          'kw': {},
                          'order': 0,
                         })

    #TODO: coverage


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ConfigurationContextTests),
        unittest.makeSuite(ConfigurationAdapterRegistryTests),
        unittest.makeSuite(ConfigurationMachineTests),
        ))
