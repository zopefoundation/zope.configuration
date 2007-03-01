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
      description=open("README.txt").read(),
      long_description=open("src/zope/configuration/README.txt").read(),
      author='Zope Project',
      author_email='zope3-dev@zope.org',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      tests_require = ['zope.testing'],
      install_requires=['zope.deprecation',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.schema',
                        'setuptools',
                       ],
      include_package_data = True,
      zip_safe = False,
      keywords="zope zope3 configuration",
      )
