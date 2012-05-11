:mod:`zope.configuration.fields`
================================

.. module:: zope.configuration.fields

.. autoclass:: PythonIdentifier
   :members:
   :member-order: bysource

   Let's look at an example:

   .. doctest::

      >>> from zope.configuration.fields import PythonIdentifier
      >>> class FauxContext(object):
      ...     pass
      >>> context = FauxContext()
      >>> field = PythonIdentifier().bind(context)

   Let's test the fromUnicode method:

   .. doctest::

      >>> field.fromUnicode(u'foo')
      u'foo'
      >>> field.fromUnicode(u'foo3')
      u'foo3'
      >>> field.fromUnicode(u'_foo3')
      u'_foo3'

   Now let's see whether validation works alright

   .. doctest::

      >>> for value in (u'foo', u'foo3', u'foo_', u'_foo3', u'foo_3', u'foo3_'):
      ...     field._validate(value)
      >>> from zope.schema import ValidationError
      >>> for value in (u'3foo', u'foo:', u'\\', u''):
      ...     try:
      ...         field._validate(value)
      ...     except ValidationError:
      ...         print 'Validation Error'
      Validation Error
      Validation Error
      Validation Error
      Validation Error

.. autoclass:: GlobalObject
   :members:
   :member-order: bysource

   Let's look at an example:

   .. doctest::

      >>> d = {'x': 1, 'y': 42, 'z': 'zope'}
      >>> class fakeresolver(dict):
      ...     def resolve(self, n):
      ...         return self[n]
      >>> fake = fakeresolver(d)

      >>> from zope.schema import Int
      >>> from zope.configuration.fields import GlobalObject
      >>> g = GlobalObject(value_type=Int())
      >>> gg = g.bind(fake)
      >>> gg.fromUnicode("x")
      1
      >>> gg.fromUnicode("   x  \n  ")
      1
      >>> gg.fromUnicode("y")
      42
      >>> gg.fromUnicode("z")
      Traceback (most recent call last):
      ...
      WrongType: ('zope', (<type 'int'>, <type 'long'>), '')

      >>> g = GlobalObject(constraint=lambda x: x%2 == 0)
      >>> gg = g.bind(fake)
      >>> gg.fromUnicode("x")
      Traceback (most recent call last):
      ...
      ConstraintNotSatisfied: 1
      >>> gg.fromUnicode("y")
      42
      >>> g = GlobalObject()
      >>> gg = g.bind(fake)
      >>> print gg.fromUnicode('*')
      None

.. autoclass:: GlobalInterface
   :members:
   :member-order: bysource

   Example:

   First, we need to set up a stub name resolver:

   .. doctest::

      >>> from zope.interface import Interface
      >>> class IFoo(Interface):
      ...     pass
      >>> class Foo(object):
      ...     pass
      >>> d = {'Foo': Foo, 'IFoo': IFoo}
      >>> class fakeresolver(dict):
      ...     def resolve(self, n):
      ...         return self[n]
      >>> fake = fakeresolver(d)

   Now verify constraints are checked correctly:

   .. doctest::

      >>> from zope.configuration.fields import GlobalInterface
      >>> g = GlobalInterface()
      >>> gg = g.bind(fake)
      >>> gg.fromUnicode('IFoo') is IFoo
      True
      >>> gg.fromUnicode('  IFoo  ') is IFoo
      True
      >>> gg.fromUnicode('Foo')
      Traceback (most recent call last):
      ...
      WrongType: ('An interface is required', ...

.. autoclass:: Tokens
   :members:
   :member-order: bysource

   Consider GlobalObject tokens:

   First, we need to set up a stub name resolver:

   .. doctest::

      >>> d = {'x': 1, 'y': 42, 'z': 'zope', 'x.y.x': 'foo'}
      >>> class fakeresolver(dict):
      ...     def resolve(self, n):
      ...         return self[n]
      >>> fake = fakeresolver(d)

      >>> from zope.configuration.fields import Tokens
      >>> from zope.configuration.fields import GlobalObject
      >>> g = Tokens(value_type=GlobalObject())
      >>> gg = g.bind(fake)
      >>> gg.fromUnicode("  \n  x y z  \n")
      [1, 42, 'zope']

      >>> from zope.schema import Int
      >>> g = Tokens(value_type=
      ...            GlobalObject(value_type=
      ...                         Int(constraint=lambda x: x%2 == 0)))
      >>> gg = g.bind(fake)
      >>> gg.fromUnicode("x y")
      Traceback (most recent call last):
      ...
      InvalidToken: 1 in x y

      >>> gg.fromUnicode("z y")
      Traceback (most recent call last):
      ...
      InvalidToken: ('zope', (<type 'int'>, <type 'long'>), '') in z y
      >>> gg.fromUnicode("y y")
      [42, 42]

.. autoclass:: Path
   :members:
   :member-order: bysource

   Let's look at an example:

   First, we need a "context" for the field that has a path
   function for converting relative path to an absolute path.

   We'll be careful to do this in an os-independent fashion.

   .. doctest::

      >>> from zope.configuration.fields import Path
      >>> class FauxContext(object):
      ...    def path(self, p):
      ...       return os.path.join(os.sep, 'faux', 'context', p)
      >>> context = FauxContext()
      >>> field = Path().bind(context)

   Lets try an absolute path first:

   .. doctest::

      >>> import os
      >>> p = unicode(os.path.join(os.sep, 'a', 'b'))
      >>> n = field.fromUnicode(p)
      >>> n.split(os.sep)
      [u'', u'a', u'b']

   This should also work with extra spaces around the path:

   .. doctest::

      >>> p = "   \n   %s   \n\n   " % p
      >>> n = field.fromUnicode(p)
      >>> n.split(os.sep)
      [u'', u'a', u'b']

   Now try a relative path:

   .. doctest::

      >>> p = unicode(os.path.join('a', 'b'))
      >>> n = field.fromUnicode(p)
      >>> n.split(os.sep)
      [u'', u'faux', u'context', u'a', u'b']

.. autoclass:: Bool
   :members:
   :member-order: bysource

   .. doctest::

      >>> from zope.configuration.fields import Bool
      >>> Bool().fromUnicode(u"yes")
      True
      >>> Bool().fromUnicode(u"y")
      True
      >>> Bool().fromUnicode(u"true")
      True
      >>> Bool().fromUnicode(u"no")
      False

.. autoclass:: MessageID
   :members:
   :member-order: bysource

   .. doctest::

      >>> from zope.configuration.fields import MessageID
      >>> class Info(object):
      ...     file = 'file location'
      ...     line = 8
      >>> class FauxContext(object):
      ...     i18n_strings = {}
      ...     info = Info()
      >>> context = FauxContext()
      >>> field = MessageID().bind(context)

   There is a fallback domain when no domain has been specified.

   Exchange the warn function so we can make test whether the warning
   has been issued

   .. doctest::

      >>> warned = None
      >>> def fakewarn(*args, **kw): #* syntax highlighting
      ...     global warned
      ...     warned = args

      >>> import warnings
      >>> realwarn = warnings.warn
      >>> warnings.warn = fakewarn

      >>> i = field.fromUnicode(u"Hello world!")
      >>> i
      u'Hello world!'
      >>> i.domain
      'untranslated'
      >>> warned
      ("You did not specify an i18n translation domain for the '' field in file location",)

      >>> warnings.warn = realwarn

   With the domain specified:

   .. doctest::

      >>> context.i18n_strings = {}
      >>> context.i18n_domain = 'testing'

   We can get a message id:

   .. doctest::

      >>> i = field.fromUnicode(u"Hello world!")
      >>> i
      u'Hello world!'
      >>> i.domain
      'testing'

   In addition, the string has been registered with the context:

   .. doctest::

      >>> context.i18n_strings
      {'testing': {u'Hello world!': [('file location', 8)]}}

      >>> i = field.fromUnicode(u"Foo Bar")
      >>> i = field.fromUnicode(u"Hello world!")
      >>> from pprint import PrettyPrinter
      >>> pprint=PrettyPrinter(width=70).pprint
      >>> pprint(context.i18n_strings)
      {'testing': {u'Foo Bar': [('file location', 8)],
                   u'Hello world!': [('file location', 8),
                                     ('file location', 8)]}}

      >>> from zope.i18nmessageid import Message
      >>> isinstance(context.i18n_strings['testing'].keys()[0], Message)
      True

   Explicit Message IDs

   .. doctest::

      >>> i = field.fromUnicode(u'[View-Permission] View')
      >>> i
      u'View-Permission'
      >>> i.default
      u'View'

      >>> i = field.fromUnicode(u'[] [Some] text')
      >>> i
      u'[Some] text'
      >>> i.default is None
      True
