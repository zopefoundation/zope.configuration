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

from zope.configuration._compat import u

NS = u('ns')
FOO = u('foo')
XXX = u('xxx')
SPLAT = u('splat')
SPLATV = u('splatv')
A = u('a')
AVALUE = u('avalue')
B = u('b')
BVALUE = u('bvalue')


class _Catchable(object):
    # Mixin for classes which need to make assertions about the exception
    # instance.
    def assertRaises(self, excClass, callableObj, *args, **kwargs):
        # Morph stdlib version to return the raised exception
        try:
            callableObj(*args, **kwargs)
        except excClass as exc:
            return exc
        if hasattr(excClass,'__name__'):
            excName = excClass.__name__
        else:
            excName = str(excClass)
        raise self.failureException("%s not raised" % excName)


class ZopeXMLConfigurationErrorTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        return ZopeXMLConfigurationError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test___str___uses_repr_of_info(self):
        zxce = self._makeOne('info', Exception, 'value')
        self.assertEqual(str(zxce), "'info'\n    Exception: value")


class ZopeSAXParseExceptionTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ZopeSAXParseException
        return ZopeSAXParseException

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test___str___not_a_sax_error(self):
        zxce = self._makeOne(Exception('Not a SAX error'))
        self.assertEqual(str(zxce), "Not a SAX error")

    def test___str___w_a_sax_error(self):
        zxce = self._makeOne(Exception('filename.xml:24:32:WAAA'))
        self.assertEqual(str(zxce), 'File "filename.xml", line 24.32, WAAA')


class ParserInfoTests(unittest.TestCase):

    _tempdir = None

    def tearDown(self):
        if self._tempdir is not None:
            import shutil
            shutil.rmtree(self._tempdir)

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ParserInfo
        return ParserInfo

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test___repr___w_eline_ecolumn_match_line_column(self):
        pi = self._makeOne('filename.xml', 24, 32)
        pi.end(24, 32)
        self.assertEqual(repr(pi), 'File "filename.xml", line 24.32')

    def test___repr___w_eline_ecolumn_dont_match_line_column(self):
        pi = self._makeOne('filename.xml', 24, 32)
        pi.end(33, 21)
        self.assertEqual(repr(pi), 'File "filename.xml", line 24.32-33.21')

    def test___str___w_eline_ecolumn_match_line_column(self):
        pi = self._makeOne('filename.xml', 24, 32)
        pi.end(24, 32)
        self.assertEqual(str(pi), 'File "filename.xml", line 24.32')

    def test___str___w_eline_ecolumn_dont_match_line_column_bad_file(self):
        pi = self._makeOne('/path/to/nonesuch.xml', 24, 32)
        pi.end(33, 21)
        self.assertEqual(str(pi),
                        'File "/path/to/nonesuch.xml", line 24.32-33.21\n'
                        '  Could not read source.')

    def test___str___w_good_file(self):
        pi = self._makeOne('tests//sample.zcml', 3, 2)
        pi.end(3, 57)
        self.assertEqual(
            str(pi),
            'File "tests//sample.zcml", line 3.2-3.57\n'
            '    <directives namespace="http://namespaces.zope.org/zope">')


class ConfigurationHandlerTests(_Catchable, unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ConfigurationHandler
        return ConfigurationHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertTrue(handler.context is context)
        self.assertFalse(handler.testing)
        self.assertEqual(handler.ignore_depth, 0)

    def test_ctor_explicit(self):
        context = FauxContext()
        handler = self._makeOne(context, True)
        self.assertTrue(handler.context is context)
        self.assertTrue(handler.testing)
        self.assertEqual(handler.ignore_depth, 0)
        self.assertTrue(handler.locator is None)

    def test_setDocumentLocator(self):
        context = FauxContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context, True)
        handler.setDocumentLocator(locator)
        self.assertTrue(handler.locator is locator)

    def test_startElementNS_w_zcml_condition_failing(self):
        from zope.configuration.xmlconfig import ZCML_CONDITION
        context = FauxContext()
        handler = self._makeOne(context, True)
        # No locator set:  we won't need it, due to a failed condition.
        handler.startElementNS((NS, FOO), FOO,
                               {ZCML_CONDITION: 'have nonesuch',
                                (None, A): AVALUE,
                                (None, B): BVALUE,
                               })
        self.assertEqual(handler.ignore_depth, 1)

    def test_startElementNS_w_ignore_depth_already_set(self):
        context = FauxContext()
        handler = self._makeOne(context, True)
        handler.ignore_depth = 1
        # No locator set:  we won't need it, as an ancestor had a
        # failed condition.
        handler.startElementNS((NS, FOO), FOO,
                               {(XXX, SPLAT): SPLATV,
                                (None, A): AVALUE,
                                (None, B): BVALUE,
                               })
        self.assertEqual(handler.ignore_depth, 2)

    def test_startElementNS_context_begin_raises_wo_testing(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        class ErrorContext(FauxContext):
          def begin(self, *args):
            raise AttributeError("xxx")
        context = ErrorContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)
        exc = self.assertRaises(ZopeXMLConfigurationError,
                    handler.startElementNS, (NS, FOO), FOO,
                                     {(XXX, SPLAT): SPLATV,
                                      (None, A): AVALUE,
                                      (None, B): BVALUE,
                                     })
        self.assertEqual(exc.info.file, 'tests//sample.zcml')
        self.assertEqual(exc.info.line, 1)
        self.assertEqual(exc.info.column, 1)

    def test_startElementNS_context_begin_raises_w_testing(self):
        class ErrorContext(FauxContext):
          def begin(self, *args):
            raise AttributeError("xxx")
        context = ErrorContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context, True)
        handler.setDocumentLocator(locator)
        self.assertRaises(AttributeError,
                    handler.startElementNS, (NS, FOO), FOO,
                                     {(XXX, SPLAT): SPLATV,
                                      (None, A): AVALUE,
                                      (None, B): BVALUE,
                                     })

    def test_startElementNS_normal(self):
        # Integration test of startElementNS / endElementNS pair.
        context = FauxContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)

        handler.startElementNS((NS, FOO), FOO,
                               {(XXX, SPLAT): SPLATV,
                                (None, A): AVALUE,
                                (None, B): BVALUE,
                               })
        self.assertEqual(context.info.file, 'tests//sample.zcml')
        self.assertEqual(context.info.line, 1)
        self.assertEqual(context.info.column, 1)
        self.assertEqual(context.begin_args,
                         ((NS, FOO),
                          {'a': AVALUE, 'b': BVALUE}))
        self.assertFalse(context._end_called)

    def test_endElementNS_w_ignore_depth_already_set(self):
        context = FauxContext()
        handler = self._makeOne(context, True)
        handler.ignore_depth = 1
        # No locator set:  we won't need it, as we had a
        # failed condition.
        handler.endElementNS((NS, FOO), FOO)
        self.assertEqual(handler.ignore_depth, 0)

    def test_endElementNS_context_end_raises_wo_testing(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        class ErrorContext(FauxContext):
          def end(self):
            raise AttributeError("xxx")
        class Info(object):
            _line = _col = None
            def end(self, line, col):
                self._line, self._col = line, col
        context = ErrorContext()
        info = Info()
        context.setInfo(info)
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)
        locator.line, locator.column = 7, 16
        exc = self.assertRaises(ZopeXMLConfigurationError,
                          handler.endElementNS, (NS, FOO), FOO)
        self.assertTrue(exc.info is context.info)
        self.assertEqual(exc.info._line, 7)
        self.assertEqual(exc.info._col, 16)

    def test_endElementNS_context_end_raises_w_testing(self):
        class ErrorContext(FauxContext):
          def end(self):
            raise AttributeError("xxx")
        class Info(object):
            _line = _col = None
            def end(self, line, col):
                self._line, self._col = line, col
        context = ErrorContext()
        info = Info()
        context.setInfo(info)
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context, True)
        handler.setDocumentLocator(locator)
        locator.line, locator.column = 7, 16
        self.assertRaises(AttributeError,
                          handler.endElementNS, (NS, FOO), FOO)
        self.assertEqual(context.info._line, 7)
        self.assertEqual(context.info._col, 16)

    def test_evaluateCondition_w_have_no_args(self):
        context = FauxContext()
        handler = self._makeOne(context)
        exc = self.assertRaises(ValueError,
                                handler.evaluateCondition, 'have')
        self.assertEqual(str(exc.args[0]), "Feature name missing: 'have'")

    def test_evaluateCondition_w_not_have_too_many_args(self):
        context = FauxContext()
        handler = self._makeOne(context)
        exc = self.assertRaises(ValueError,
                                handler.evaluateCondition, 'not-have a b')
        self.assertEqual(str(exc.args[0]),
                         "Only one feature allowed: 'not-have a b'")

    def test_evaluateCondition_w_have_miss(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertFalse(handler.evaluateCondition('have feature'))

    def test_evaluateCondition_w_have_hit(self):
        context = FauxContext()
        context._features = ('feature',)
        handler = self._makeOne(context)
        self.assertTrue(handler.evaluateCondition('have feature'))

    def test_evaluateCondition_w_not_have_miss(self):
        context = FauxContext()
        context._features = ('feature',)
        handler = self._makeOne(context)
        self.assertFalse(handler.evaluateCondition('not-have feature'))

    def test_evaluateCondition_w_not_have_hit(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertTrue(handler.evaluateCondition('not-have feature'))

    def test_evaluateCondition_w_installed_no_args(self):
        context = FauxContext()
        handler = self._makeOne(context)
        exc = self.assertRaises(ValueError,
                                handler.evaluateCondition, 'installed')
        self.assertEqual(str(exc.args[0]), "Package name missing: 'installed'")

    def test_evaluateCondition_w_not_installed_too_many_args(self):
        context = FauxContext()
        handler = self._makeOne(context)
        exc = self.assertRaises(ValueError,
                                handler.evaluateCondition, 'not-installed a b')
        self.assertEqual(str(exc.args[0]),
                         "Only one package allowed: 'not-installed a b'")

    def test_evaluateCondition_w_installed_miss(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertFalse(handler.evaluateCondition('installed nonsuch.package'))

    def test_evaluateCondition_w_installed_hit(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertTrue(handler.evaluateCondition('installed os'))

    def test_evaluateCondition_w_not_installed_miss(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertFalse(handler.evaluateCondition('not-installed os'))

    def test_evaluateCondition_w_not_installed_hit(self):
        context = FauxContext()
        handler = self._makeOne(context)
        self.assertTrue(
                handler.evaluateCondition('not-installed nonsuch.package'))

    def test_evaluateCondition_w_unknown_verb(self):
        context = FauxContext()
        handler = self._makeOne(context)
        exc = self.assertRaises(ValueError,
                                handler.evaluateCondition, 'nonesuch')
        self.assertEqual(str(exc.args[0]),
                         "Invalid ZCML condition: 'nonesuch'")

    def test_endElementNS_normal(self):
        class Info(object):
            _line = _col = None
            def end(self, line, col):
                self._line, self._col = line, col
        context = FauxContext()
        info = Info()
        context.setInfo(info)
        locator = FauxLocator('tests//sample.zcml', 7, 16)
        handler = self._makeOne(context, True)
        handler.setDocumentLocator(locator)
        handler.endElementNS((NS, FOO), FOO)
        self.assertEqual(context.info._line, 7)
        self.assertEqual(context.info._col, 16)
        self.assertTrue(context._end_called)


class Test_processxmlfile(_Catchable, unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import processxmlfile
        return processxmlfile(*args, **kw)

    def test_w_empty_xml(self):
        from StringIO import StringIO
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives
        from zope.configuration.xmlconfig import ZopeSAXParseException
        context = ConfigurationMachine()
        registerCommonDirectives(context)
        exc = self.assertRaises(ZopeSAXParseException,
                                self._callFUT, StringIO(), context)
        self.assertEqual(str(exc._v), '<string>:1:0: no element found')

    def test_w_valid_xml_fp(self):
        # Integration test, really
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        file = open(path("samplepackage", "configure.zcml"))
        context = ConfigurationMachine()
        registerCommonDirectives(context)
        self._callFUT(file, context)
        self.assertEqual(foo.data, [])
        context.execute_actions()
        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('blah')), ('y', 0)))
        self.assertEqual(clean_info_path(repr(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29')
        self.assertEqual(clean_info_path(str(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29\n'
                + '    <test:foo x="blah" y="0" />')
        self.assertEqual(data.package, None)
        self.assertEqual(data.basepath, None)


class Test_openInOrPlain(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import openInOrPlain
        return openInOrPlain(*args, **kw)


class Test_include(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import include
        return include(*args, **kw)

    def test_include_by_package(self):
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        import zope.configuration.tests.samplepackage as package
        context = ConfigurationMachine()
        registerCommonDirectives(context)
        self._callFUT(context, 'configure.zcml', package)
        context.execute_actions()
        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('blah')), ('y', 0)))
        self.assertEqual(clean_info_path(repr(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29')
        self.assertEqual(clean_info_path(str(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29\n'
                + '    <test:foo x="blah" y="0" />')
        self.assertTrue(data.package is package)
        self.assertEqual(data.basepath[-13:], 'samplepackage')
        self.assertEqual([clean_path(p) for p in data.includepath],
                         ['tests/samplepackage/configure.zcml'])

    # Not any more
    ##     Including the same file more than once produces an error:

    ##     >>> try:
    ##     ...   xmlconfig.include(context, 'configure.zcml', package)
    ##     ... except xmlconfig.ConfigurationError, e:
    ##     ...   'OK'
    ##     ...
    ##     'OK'

    def test_include_by_file(self):
        import os
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        context = ConfigurationMachine()
        registerCommonDirectives(context)
        here = os.path.dirname(__file__)
        path = os.path.join(here, "samplepackage", "foo.zcml")
        self._callFUT(context, path)
        context.execute_actions()
        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('foo')), ('y', 2)))
        self.assertEqual(clean_info_path(repr(data.info)),
                    'File "tests/samplepackage/foo.zcml.in", line 12.2-12.28')
        self.assertEqual(clean_info_path(str(data.info)),
                    'File "tests/samplepackage/foo.zcml.in", line 12.2-12.28\n'
                    + '    <test:foo x="foo" y="2" />')
        self.assertEqual(data.package, None)
        self.assertEqual(data.basepath[-13:], 'samplepackage')
        self.assertEqual([clean_path(p) for p in data.includepath],
                         ['tests/samplepackage/foo.zcml.in'])

    def test_include_by_file_glob(self):
        import os
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        context = ConfigurationMachine()
        registerCommonDirectives(context)
        here = os.path.dirname(__file__)
        path = os.path.join(here, "samplepackage/baz*.zcml")
        self._callFUT(context, files=path)
        context.execute_actions()

        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('foo')), ('y', 3)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/baz3.zcml", line 5.2-5.28')

        self.assertEqual(clean_info_path(str(data.info)), 
                        'File "tests/samplepackage/baz3.zcml", line 5.2-5.28\n'
                        + '    <test:foo x="foo" y="3" />')
        self.assertEqual(data.package, None)
        self.assertEqual(data.basepath[-13:], 'samplepackage')
        self.assertEqual([clean_path(p) for p in data.includepath],
                         ['tests/samplepackage/baz3.zcml'])

        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('foo')), ('y', 2)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/baz2.zcml", line 5.2-5.28')
        self.assertEqual(clean_info_path(str(data.info)),
                        'File "tests/samplepackage/baz2.zcml", line 5.2-5.28\n'
                        + '    <test:foo x="foo" y="2" />')
        self.assertEqual(data.package, None)
        self.assertEqual(data.basepath[-13:], 'samplepackage')
        self.assertEqual([clean_path(p) for p in data.includepath],
                        ['tests/samplepackage/baz2.zcml'])


class Test_exclude(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import exclude
        return exclude(*args, **kw)


class Test_includeOverrides(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import includeOverrides
        return includeOverrides(*args, **kw)


class Test_file(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import file
        return file(*args, **kw)

    def test_simple(self):
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        file_name = path("samplepackage", "configure.zcml")
        context = self._callFUT(file_name)
        data = foo.data.pop()
        self.assertEqual(data.args, (('x', b('blah')), ('y', 0)))
        self.assertEqual(clean_info_path(repr(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29')
        self.assertEqual(clean_info_path(str(data.info)),
                'File "tests/samplepackage/configure.zcml", line 12.2-12.29\n' +
                '    <test:foo x="blah" y="0" />')
        self.assertEqual(data.package, None)
        self.assertEqual(clean_path(data.basepath),
                         'tests/samplepackage')


class Test_string(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import string
        return string(*args, **kw)


class XMLConfigTests(unittest.TestCase):

    def setUp(self):
        from zope.configuration.xmlconfig import _clearContext
        _clearContext()

    def tearDown(self):
        from zope.configuration.xmlconfig import _clearContext
        _clearContext()

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import XMLConfig
        return XMLConfig

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_XMLConfig(self):
        import os
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        here = os.path.dirname(__file__)
        path = os.path.join(here, "samplepackage", "baro.zcml")
        x = self._makeOne(path)
        x() # call to process the actions
        self.assertEqual(len(foo.data), 3)

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 0)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/bar21.zcml", line 3.2-3.24')

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 2)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/bar2.zcml", line 5.2-5.24')

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 1)))
        self.assertEqual(clean_info_path(repr(data.info)),
                         'File "tests/samplepackage/bar2.zcml", line 6.2-6.24')

    def test_XMLConfig_w_module(self):
        from zope.configuration._compat import b
        from zope.configuration.tests.samplepackage import foo
        from zope.configuration.tests import samplepackage as module
        x = self._makeOne("baro.zcml", module)
        x() # call to process the actions
        self.assertEqual(len(foo.data), 3)

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 0)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/bar21.zcml", line 3.2-3.24')

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 2)))
        self.assertEqual(clean_info_path(repr(data.info)),
                        'File "tests/samplepackage/bar2.zcml", line 5.2-5.24')

        data = foo.data.pop(0)
        self.assertEqual(data.args, (('x', b('blah')), ('y', 1)))
        self.assertEqual(clean_info_path(repr(data.info)),
                         'File "tests/samplepackage/bar2.zcml", line 6.2-6.24')


class Test_xmlconfig(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import xmlconfig
        return xmlconfig(*args, **kw)


class Test_testxmlconfig(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import testxmlconfig
        return testxmlconfig(*args, **kw)



class FauxLocator(object):
    def __init__(self, file, line, column):
        self.file, self.line, self.column = file, line, column
    def getSystemId(self):
        return self.file
    def getLineNumber(self):
        return self.line
    def getColumnNumber(self):
        return self.column


class FauxContext(object):
    _features = ()
    _end_called = False
    def setInfo(self, info):
        self.info = info
    def getInfo(self):
        return self.info
    def begin(self, name, data, info):
        self.begin_args = name, data
        self.info = info
    def end(self):
        self._end_called = 1
    def hasFeature(self, feature):
        return feature in self._features


def path(*p):
    import os
    return os.path.join(os.path.dirname(__file__), *p)

def clean_info_path(s):
    import os
    part1 = s[:6]
    part2 = s[6:s.find('"', 6)]
    part2 = part2[part2.rfind("tests"):]
    part2 = part2.replace(os.sep, '/')
    part3 = s[s.find('"', 6):].rstrip()
    return part1+part2+part3

def clean_path(s):
    import os
    s = s[s.rfind("tests"):]
    s = s.replace(os.sep, '/')
    return s

def clean_actions(actions):
    return [
      {'discriminator': action['discriminator'],
       'info': clean_info_path(repr(action['info'])),
       'includepath': [clean_path(p) for p in action['includepath']],
       }
      for action in actions
      ]

def clean_text_w_paths(error):
    r = []
    for line in unicode(error).split("\n"):
      line = line.rstrip()
      if not line:
        continue
      l = line.find('File "')
      if l >= 0:
        line = line[:l] + clean_info_path(line[l:])
      r.append(line)
    return '\n'.join(r)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ZopeXMLConfigurationErrorTests),
        unittest.makeSuite(ZopeSAXParseExceptionTests),
        unittest.makeSuite(ParserInfoTests),
        unittest.makeSuite(ConfigurationHandlerTests),
        unittest.makeSuite(Test_processxmlfile),
        unittest.makeSuite(Test_openInOrPlain),
        unittest.makeSuite(Test_include),
        unittest.makeSuite(Test_exclude),
        unittest.makeSuite(Test_includeOverrides),
        unittest.makeSuite(Test_file),
        unittest.makeSuite(Test_string),
        unittest.makeSuite(XMLConfigTests),
        unittest.makeSuite(Test_xmlconfig),
        unittest.makeSuite(Test_testxmlconfig),
    ))
