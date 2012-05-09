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


class ZopeXMLConfigurationErrorTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        return ZopeXMLConfigurationError

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class ZopeSAXParseExceptionTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ZopeSAXParseException
        return ZopeSAXParseException

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class ParserInfoTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ParserInfo
        return ParserInfo

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


class ConfigurationHandlerTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.configuration.xmlconfig import ConfigurationHandler
        return ConfigurationHandler

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_normal(self):
        context = FauxContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)

        handler.startElementNS((NS, FOO), FOO,
                               {(XXX, SPLAT): SPLATV,
                                (None, A): AVALUE,
                                (None, B): BVALUE,
                               })
        self.assertEqual(repr(context.info),
                         'File "tests//sample.zcml", line 1.1')
        self.assertEqual(context.begin_args,
                         ((NS, FOO),
                          {'a': AVALUE, 'b': BVALUE}))
        self.assertEqual(getattr(context, "end_called", 0), 0)

        locator.line, locator.column = 7, 16
        handler.endElementNS((NS, FOO), FOO)
        self.assertEqual(repr(context.info),
                         'File "tests//sample.zcml", line 1.1-7.16')
        self.assertEqual(context.end_called, 1)

    def test_err_start(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        class ErrorContext(FauxContext):
          def begin(self, *args):
            raise AttributeError("xxx")
        context = ErrorContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)
        self.assertRaises(ZopeXMLConfigurationError,
                    handler.startElementNS, (NS, FOO), FOO,
                                     {(XXX, SPLAT): SPLATV,
                                      (None, A): AVALUE,
                                      (None, B): BVALUE,
                                     })

    def test_err_end(self):
        from zope.configuration.xmlconfig import ZopeXMLConfigurationError
        class ErrorContext(FauxContext):
          def end(self):
            raise AttributeError("xxx")
        context = ErrorContext()
        locator = FauxLocator('tests//sample.zcml', 1, 1)
        handler = self._makeOne(context)
        handler.setDocumentLocator(locator)
        handler.startElementNS((NS, FOO), FOO,
                               {(XXX, SPLAT): SPLATV,
                                (None, A): AVALUE,
                                (None, B): BVALUE,
                               })

        locator.line, locator.column = 7, 16
        self.assertRaises(ZopeXMLConfigurationError,
                          handler.endElementNS, (NS, FOO), FOO)


class Test_processxmlfile(unittest.TestCase):

    def _callFUT(self, *args, **kw):
        from zope.configuration.xmlconfig import processxmlfile
        return processxmlfile(*args, **kw)

    def test_it(self):
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

  def setInfo(self, info):
    self.info = info
  def getInfo(self):
    return self.info
  def begin(self, name, data, info):
    self.begin_args = name, data
    self.info = info
  def end(self):
    self.end_called = 1


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
