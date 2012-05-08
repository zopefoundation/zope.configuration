:mod:`zope.configuration.xmlconfig`
===================================

.. module:: zope.configuration.xmlconfig

.. autoclass:: ZopeXMLConfigurationError

   Example

   .. doctest::

      >>> from zope.configuration.xmlconfig import ZopeXMLConfigurationError
      >>> v = ZopeXMLConfigurationError("blah", AttributeError, "xxx")
      >>> print v
      'blah'
          AttributeError: xxx

.. autoclass:: ZopeSAXParseException

   Example

   .. doctest::

      >>> from zope.configuration.xmlconfig import ZopeSAXParseException
      >>> v = ZopeSAXParseException("foo.xml:12:3:Not well formed")
      >>> print v
      File "foo.xml", line 12.3, Not well formed

.. autoclass:: ParserInfo
   :members:
   :member-order: bysource

   Example

   .. doctest::

      >>> from zope.configuration.xmlconfig import ParserInfo
      >>> info = ParserInfo('tests//sample.zcml', 1, 0)
      >>> info
      File "tests//sample.zcml", line 1.0

      >>> print info
      File "tests//sample.zcml", line 1.0

      >>> info.characters("blah\\n")
      >>> info.characters("blah")
      >>> info.text
      u'blah\\nblah'

      >>> info.end(7, 0)
      >>> info
      File "tests//sample.zcml", line 1.0-7.0

      >>> print info
      File "tests//sample.zcml", line 1.0-7.0
        <configure xmlns='http://namespaces.zope.org/zope'>
          <!-- zope.configure -->
          <directives namespace="http://namespaces.zope.org/zope">
            <directive name="hook" attributes="name implementation module"
               handler="zope.configuration.metaconfigure.hook" />
          </directives>
        </configure>

.. autoclass:: ConfigurationHandler

   .. automethod:: evaluateCondition

      The ``have`` and ``not-have`` verbs each take one argument: the name
      of a feature:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> from zope.configuration.xmlconfig import ConfigurationHandler
         >>> context = ConfigurationContext()
         >>> context.provideFeature('apidoc')
         >>> c = ConfigurationHandler(context, testing=True)
         >>> c.evaluateCondition("have apidoc")
         True
         >>> c.evaluateCondition("not-have apidoc")
         False
         >>> c.evaluateCondition("have onlinehelp")
         False
         >>> c.evaluateCondition("not-have onlinehelp")
         True

      Ill-formed expressions raise an error:

      .. doctest::

         >>> c.evaluateCondition("want apidoc")
         Traceback (most recent call last):
           ...
         ValueError: Invalid ZCML condition: 'want apidoc'

         >>> c.evaluateCondition("have x y")
         Traceback (most recent call last):
           ...
         ValueError: Only one feature allowed: 'have x y'

         >>> c.evaluateCondition("have")
         Traceback (most recent call last):
           ...
         ValueError: Feature name missing: 'have'


      The ``installed`` and ``not-installed`` verbs each take one argument:
      the dotted name of a pacakge.
      
      If the pacakge is found, in other words, can be imported,
      then the condition will return true / false:

      .. doctest::

         >>> context = ConfigurationContext()
         >>> c = ConfigurationHandler(context, testing=True)
         >>> c.evaluateCondition('installed zope.interface')
         True
         >>> c.evaluateCondition('not-installed zope.interface')
         False
         >>> c.evaluateCondition('installed zope.foo')
         False
         >>> c.evaluateCondition('not-installed zope.foo')
         True

      Ill-formed expressions raise an error:

      .. doctest::

         >>> c.evaluateCondition("installed foo bar")
         Traceback (most recent call last):
           ...
         ValueError: Only one package allowed: 'installed foo bar'

         >>> c.evaluateCondition("installed")
         Traceback (most recent call last):
           ...
         ValueError: Package name missing: 'installed'

.. autofunction:: processxmlfile

.. autofunction:: openInOrPlain

   For example, the tests/samplepackage dirextory has files:

   - configure.zcml
   - configure.zcml.in
   - foo.zcml.in

   If we open configure.zcml, we'll get that file:

   .. doctest::

      >>> import os
      >>> from zope.configuration.xmlconfig import __file__
      >>> from zope.configuration.xmlconfig import openInOrPlain
      >>> here = os.path.dirname(__file__)
      >>> path = os.path.join(here, 'tests', 'samplepackage', 'configure.zcml')
      >>> f = openInOrPlain(path)
      >>> f.name[-14:]
      'configure.zcml'

   But if we open foo.zcml, we'll get foo.zcml.in, since there isn't a
   foo.zcml:

   .. doctest::

      >>> path = os.path.join(here, 'tests', 'samplepackage', 'foo.zcml')
      >>> f = openInOrPlain(path)
      >>> f.name[-11:]
      'foo.zcml.in'

   Make sure other IOErrors are re-raised.  We need to do this in a
   try-except block because different errors are raised on Windows and
   on Linux.

   .. doctest::

      >>> try:
      ...     f = openInOrPlain('.')
      ... except IOError:
      ...     print "passed"
      ... else:
      ...     print "failed"
      passed

.. autointerface:: IInclude
   :members:
   :member-order: bysource

.. autofunction:: include

.. autofunction:: exclude

.. autofunction:: includeOverrides

.. autofunction:: registerCommonDirectives
