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

import sys
import unittest
import re
from doctest import DocTestSuite
from zope.testing import renormalizing
from zope.configuration.config import metans, ConfigurationMachine
from zope.configuration import config

def test_keyword_handling():
    """
    >>> machine = ConfigurationMachine()
    >>> ns = "http://www.zope.org/testing"

    Register some test directives:

    Start with a grouping directive that sets a package:

    >>> machine((metans, "groupingDirective"),
    ...         name="package", namespace=ns,
    ...         schema="zope.configuration.tests.directives.IPackaged",
    ...         handler="zope.configuration.tests.directives.Packaged",
    ...         )

    Now we can set the package:

    >>> machine.begin((ns, "package"),
    ...               package="zope.configuration.tests.directives",
    ...               )

    Which makes it easier to define the other directives:

    >>> machine((metans, "directive"),
    ...         namespace=ns, name="k",
    ...         schema=".Ik", handler=".k")


    >>> machine((ns, "k"), "yee ha", **{"for": u"f", "class": u"c", "x": u"x"})

    >>> from pprint import PrettyPrinter
    >>> pprint=PrettyPrinter(width=60).pprint
    >>> pprint(machine.actions)
    [{'args': ('f', 'c', 'x'),
      'callable': f,
      'discriminator': ('k', 'f'),
      'includepath': (),
      'info': 'yee ha',
      'kw': {},
      'order': 0}]
    """

def test_basepath_absolute():
    """Path must always return an absolute path.

    >>> import os
    >>> class stub:
    ...     __file__ = os.path.join('relative', 'path')
    >>> c = config.ConfigurationContext()
    >>> c.package = stub()

    >>> os.path.isabs(c.path('y/z'))
    True
    """

def test_basepath_uses_dunder_path():
    """Determine package path using __path__ if __file__ isn't available.
    (i.e. namespace package installed with --single-version-externally-managed)

    >>> import os
    >>> class stub:
    ...     __path__ = [os.path.join('relative', 'path')]
    >>> c = config.ConfigurationContext()
    >>> c.package = stub()

    >>> os.path.isabs(c.path('y/z'))
    True
    """

def test_trailing_dot_in_resolve():
    """Dotted names are no longer allowed to end in dots

    >>> c = config.ConfigurationContext()

    >>> c.resolve('zope.')
    Traceback (most recent call last):
    ...
    ValueError: Trailing dots are no longer supported in dotted names

    >>> c.resolve('  ')
    Traceback (most recent call last):
    ...
    ValueError: The given name is blank
    """

def test_bad_dotted_last_import():
    """
    >>> c = config.ConfigurationContext()

    Import error caused by a bad last component in the dotted name.

    >>> c.resolve('zope.configuration.tests.nosuch')
    Traceback (most recent call last):
    ...
    ConfigurationError: ImportError: Module zope.configuration.tests""" \
                                               """ has no global nosuch
    """

def test_bad_dotted_import():
    """
    >>> c = config.ConfigurationContext()

    Import error caused by a totally wrong dotted name.

    >>> c.resolve('zope.configuration.nosuch.noreally')
    Traceback (most recent call last):
    ...
    ConfigurationError: ImportError: Couldn't import""" \
                   """ zope.configuration.nosuch, No module named nosuch
    """

def test_bad_sub_last_import():
    """
    >>> c = config.ConfigurationContext()

    Import error caused by a bad sub import inside the referenced
    dotted name. Here we keep the standard traceback.

    >>> c.resolve('zope.configuration.tests.victim')
    Traceback (most recent call last):
    ...
      File "...bad.py", line 3 in ?
       import bad_to_the_bone
    ImportError: No module named bad_to_the_bone

    Cleanup:

    >>> for name in ('zope.configuration.tests.victim',
    ...              'zope.configuration.tests.bad'):
    ...    if name in sys.modules:
    ...        del sys.modules[name]
    """

def test_bad_sub_import():
    """
    >>> c = config.ConfigurationContext()

    Import error caused by a bad sub import inside part of the referenced
    dotted name. Here we keep the standard traceback.

    >>> c.resolve('zope.configuration.tests.victim.nosuch')
    Traceback (most recent call last):
    ...
      File "...bad.py", line 3 in ?
       import bad_to_the_bone
    ImportError: No module named bad_to_the_bone

    Cleanup:

    >>> for name in ('zope.configuration.tests.victim',
    ...              'zope.configuration.tests.bad'):
    ...    if name in sys.modules:
    ...        del sys.modules[name]
    """

def test_suite():
    checker = renormalizing.RENormalizing([
        (re.compile(r"<type 'exceptions.(\w+)Error'>:"),
                    r'exceptions.\1Error:'),
        ])
    return unittest.TestSuite((
        DocTestSuite('zope.configuration.fields'),
        DocTestSuite('zope.configuration.config',checker=checker),
        DocTestSuite(),
        ))

if __name__ == '__main__': unittest.main()
