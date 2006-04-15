zope.configuration Package Readme
=================================

Overview
--------

The zope configuration system provides an extensible system for
supporting various kinds of configurations.

It is based on the idea of configuration directives. Users of the
configuration system provide configuration directives in some
language that express configuration choices. The intent is that the
language be pluggable.  An XML language is provided by default.

See 'src/zope/configuration/README.txt' for more information.

Changes
-------

See CHANGES.txt.

Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.configuration/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.configuration/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.configuration/trunk

- Note that the 'src/zope/configuration' package is acutally a
  'svn:externals' link to the corresponding package in the Zope3 trunk
  (or to a specific tag, for released versions of the package).
