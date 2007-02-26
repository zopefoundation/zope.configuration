##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.configuration package

$Id$
"""

import os

from setuptools import setup, find_packages

setup(name='zope.configuration',
      version='3.4dev',
      url='http://svn.zope.org/zope.configuration',
      license='ZPL 2.1',
      description='Zope Configuration (ZCML)',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description='''\
The zope configuration system provides an extensible system for
supporting various kinds of configurations.

It is based on the idea of configuration directives. Users of the
configuration system provide configuration directives in some
language that express configuration choices. The intent is that the
language be pluggable.  An XML language is provided by default.
      ''',
      
	  packages=find_packages('src'),
      package_dir = {'': 'src'},

      namespace_packages=['zope',],
      tests_require = ['zope.testing'],
      install_requires=['zope.deprecation',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.schema',
                       ],
      include_package_data = True,

      zip_safe = False,
      )
