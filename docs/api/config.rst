:mod:`zope.configuration.config`
================================

.. module:: zope.configuration.config

.. autoclass:: ConfigurationContext

   .. automethod:: resolve

      Examples:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> from zope.configuration.config import ConfigurationError
         >>> c = ConfigurationContext()
         >>> import zope, zope.interface
         >>> c.resolve('zope') is zope
         True
         >>> c.resolve('zope.interface') is zope.interface
         True
         >>> c.resolve('zope.configuration.eek') #doctest: +NORMALIZE_WHITESPACE
         Traceback (most recent call last):
         ...
         ConfigurationError:
         ImportError: Module zope.configuration has no global eek

         >>> c.resolve('.config.ConfigurationContext')
         Traceback (most recent call last):
         ...
         AttributeError: 'ConfigurationContext' object has no attribute 'package'
         >>> import zope.configuration
         >>> c.package = zope.configuration
         >>> c.resolve('.') is zope.configuration
         True
         >>> c.resolve('.config.ConfigurationContext') is ConfigurationContext
         True
         >>> c.resolve('..interface') is zope.interface
         True
         >>> c.resolve('str')
         <type 'str'>

   .. automethod:: path

      Examples:

      .. doctest::

         >>> import os
         >>> from zope.configuration.config import ConfigurationContext
         >>> c = ConfigurationContext()
         >>> c.path("/x/y/z") == os.path.normpath("/x/y/z")
         True
         >>> c.path("y/z")
         Traceback (most recent call last):
         ...
         AttributeError: 'ConfigurationContext' object has no attribute 'package'
         >>> import zope.configuration
         >>> c.package = zope.configuration
         >>> import os
         >>> d = os.path.dirname(zope.configuration.__file__)
         >>> c.path("y/z") == d + os.path.normpath("/y/z")
         True
         >>> c.path("y/./z") == d + os.path.normpath("/y/z")
         True
         >>> c.path("y/../z") == d + os.path.normpath("/z")
         True

   .. automethod:: checkDuplicate

      Examples:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> from zope.configuration.config import ConfigurationError
         >>> c = ConfigurationContext()
         >>> c.checkDuplicate('/foo.zcml')
         >>> try:
         ...     c.checkDuplicate('/foo.zcml')
         ... except ConfigurationError as e:
         ...     # On Linux the exact msg has /foo, on Windows \foo.
         ...     str(e).endswith("foo.zcml' included more than once")
         True

      You may use different ways to refer to the same file:

      .. doctest::

         >>> import zope.configuration
         >>> c.package = zope.configuration
         >>> import os
         >>> d = os.path.dirname(zope.configuration.__file__)
         >>> c.checkDuplicate('bar.zcml')
         >>> try:
         ...   c.checkDuplicate(d + os.path.normpath('/bar.zcml'))
         ... except ConfigurationError as e:
         ...   str(e).endswith("bar.zcml' included more than once")
         ...
         True

   .. automethod:: processFile

      Examples:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> c = ConfigurationContext()
         >>> c.processFile('/foo.zcml')
         True
         >>> c.processFile('/foo.zcml')
         False

      You may use different ways to refer to the same file:

      .. doctest::

         >>> import zope.configuration
         >>> c.package = zope.configuration
         >>> import os
         >>> d = os.path.dirname(zope.configuration.__file__)
         >>> c.processFile('bar.zcml')
         True
         >>> c.processFile('bar.zcml')
         False

   .. automethod:: action

      Examples:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> c = ConfigurationContext()

      Normally, the context gets actions from subclasses. We'll provide
      an actions attribute ourselves:

      .. doctest::

         >>> c.actions = []

      We'll use a test callable that has a convenient string representation

      .. doctest::

         >>> from zope.configuration.tests.directives import f
         >>> c.action(1, f, (1, ), {'x': 1})
         >>> from pprint import PrettyPrinter
         >>> pprint=PrettyPrinter(width=60).pprint
         >>> pprint(c.actions)
         [{'args': (1,),
           'callable': f,
           'discriminator': 1,
           'includepath': (),
           'info': '',
           'kw': {'x': 1},
           'order': 0}]

         >>> c.action(None)
         >>> pprint(c.actions)
         [{'args': (1,),
           'callable': f,
           'discriminator': 1,
           'includepath': (),
           'info': '',
           'kw': {'x': 1},
           'order': 0},
          {'args': (),
           'callable': None,
           'discriminator': None,
           'includepath': (),
           'info': '',
           'kw': {},
           'order': 0}]

      Now set the include path and info:

      .. doctest::

         >>> c.includepath = ('foo.zcml',)
         >>> c.info = "?"
         >>> c.action(None)
         >>> pprint(c.actions[-1])
         {'args': (),
          'callable': None,
          'discriminator': None,
          'includepath': ('foo.zcml',),
          'info': '?',
          'kw': {},
          'order': 0}

      We can add an order argument to crudely control the order
      of execution:

      .. doctest::

         >>> c.action(None, order=99999)
         >>> pprint(c.actions[-1])
         {'args': (),
          'callable': None,
          'discriminator': None,
          'includepath': ('foo.zcml',),
          'info': '?',
          'kw': {},
          'order': 99999}

      We can also pass an includepath argument, which will be used as the the
      includepath for the action.  (if includepath is None, self.includepath
      will be used):

      .. doctest::

         >>> c.action(None, includepath=('abc',))
         >>> pprint(c.actions[-1])
         {'args': (),
          'callable': None,
          'discriminator': None,
          'includepath': ('abc',),
          'info': '?',
          'kw': {},
          'order': 0}

      We can also pass an info argument, which will be used as the the
      source line info for the action.  (if info is None, self.info will be
      used):

      .. doctest::

         >>> c.action(None, info='abc')
         >>> pprint(c.actions[-1])
         {'args': (),
          'callable': None,
          'discriminator': None,
          'includepath': ('foo.zcml',),
          'info': 'abc',
          'kw': {},
          'order': 0}

   .. automethod:: hasFeature

      Examples:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationContext
         >>> c = ConfigurationContext()
         >>> c.hasFeature('onlinehelp')
         False

      You can declare that a feature is provided

      .. doctest::

         >>> c.provideFeature('onlinehelp')

      and it becomes available

      .. doctest::

         >>> c.hasFeature('onlinehelp')
         True

   .. automethod:: provideFeature

.. autoclass:: ConfigurationAdapterRegistry
   :members:
   :member-order: bysource

   Examples:

   .. doctest::

      >>> from zope.configuration.interfaces import IConfigurationContext
      >>> from zope.configuration.config import ConfigurationAdapterRegistry
      >>> from zope.configuration.config import ConfigurationError
      >>> from zope.configuration.config import ConfigurationMachine
      >>> r = ConfigurationAdapterRegistry()
      >>> c = ConfigurationMachine()
      >>> r.factory(c, ('http://www.zope.com','xxx'))
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Unknown directive', 'http://www.zope.com', 'xxx')
      >>> def f():
      ...     pass

      >>> r.register(IConfigurationContext, ('http://www.zope.com', 'xxx'), f)
      >>> r.factory(c, ('http://www.zope.com','xxx')) is f
      True
      >>> r.factory(c, ('http://www.zope.com','yyy')) is f
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Unknown directive', 'http://www.zope.com', 'yyy')
      >>> r.register(IConfigurationContext, 'yyy', f)
      >>> r.factory(c, ('http://www.zope.com','yyy')) is f
      True

   Test the documentation feature:

   .. doctest::

      >>> from zope.configuration.config import IFullInfo
      >>> r._docRegistry
      []
      >>> r.document(('ns', 'dir'), IFullInfo, IConfigurationContext, None,
      ...            'inf', None)
      >>> r._docRegistry[0][0] == ('ns', 'dir')
      True
      >>> r._docRegistry[0][1] is IFullInfo
      True
      >>> r._docRegistry[0][2] is IConfigurationContext
      True
      >>> r._docRegistry[0][3] is None
      True
      >>> r._docRegistry[0][4] == 'inf'
      True
      >>> r._docRegistry[0][5] is None
      True
      >>> r.document('all-dir', None, None, None, None)
      >>> r._docRegistry[1][0]
      ('', 'all-dir')

.. autoclass:: ConfigurationMachine

   Example:

   .. doctest::

      >>> from zope.configuration.config import ConfigurationMachine
      >>> machine = ConfigurationMachine()
      >>> ns = "http://www.zope.org/testing"

   Register a directive:

   .. doctest::

      >>> from zope.configuration.config import metans
      >>> machine((metans, "directive"),
      ...         namespace=ns, name="simple",
      ...         schema="zope.configuration.tests.directives.ISimple",
      ...         handler="zope.configuration.tests.directives.simple")

   and try it out:

   .. doctest::

      >>> machine((ns, "simple"), a=u"aa", c=u"cc")
      >>> from pprint import PrettyPrinter
      >>> pprint = PrettyPrinter(width=60).pprint
      >>> pprint(machine.actions)
      [{'args': (u'aa', u'xxx', 'cc'),
        'callable': f,
        'discriminator': ('simple', u'aa', u'xxx', 'cc'),
        'includepath': (),
        'info': None,
        'kw': {},
        'order': 0}]

   .. automethod:: begin

   .. automethod:: end

   .. automethod:: __call__

   .. automethod:: getInfo

   .. automethod:: setInfo

   .. automethod:: execute_actions

      For example:

      .. doctest::

         >>> from zope.configuration.config import ConfigurationMachine
         >>> output = []
         >>> def f(*a, **k): #* syntax highlighting
         ...    output.append(('f', a, k))
         >>> context = ConfigurationMachine()
         >>> context.actions = [
         ...   (1, f, (1,)),
         ...   (1, f, (11,), {}, ('x', )),
         ...   (2, f, (2,)),
         ...   ]
         >>> context.execute_actions()
         >>> output
         [('f', (1,), {}), ('f', (2,), {})]

      If the action raises an error, we convert it to a
      ConfigurationExecutionError.

      .. doctest::

         >>> from zope.configuration.config import ConfigurationExecutionError
         >>> output = []
         >>> def bad():
         ...    bad.xxx
         >>> context.actions = [
         ...   (1, f, (1,)),
         ...   (1, f, (11,), {}, ('x', )),
         ...   (2, f, (2,)),
         ...   (3, bad, (), {}, (), 'oops')
         ...   ]
         >>> try:
         ...    v = context.execute_actions()
         ... except ConfigurationExecutionError as v:
         ...    pass
         >>> lines = str(v).splitlines()
         >>> 'exceptions.AttributeError' in lines[0]
         True
         >>> lines[0].endswith("'function' object has no attribute 'xxx'")
         True
         >>> lines[1:]
         ['  in:', '  oops']

      Note that actions executed before the error still have an effect:

      .. doctest::

         >>> output
         [('f', (1,), {}), ('f', (2,), {})]

.. autoclass:: ConfigurationExecutionError

.. autointerface:: IStackItem
   :members:
   :member-order: bysource

.. autoclass:: SimpleStackItem
   :members:
   :member-order: bysource

.. autoclass:: RootStackItem
   :members:
   :member-order: bysource

.. autoclass:: GroupingStackItem
   :members:
   :member-order: bysource

   To see how this works, let's look at an example:

   We need a context. We'll just use a configuration machine

   .. doctest::

      >>> from zope.configuration.config import GroupingStackItem
      >>> from zope.configuration.config import ConfigurationMachine
      >>> context = ConfigurationMachine()

   We need a callable to use in configuration actions.  We'll use a
   convenient one from the tests:

   .. doctest::

      >>> from zope.configuration.tests.directives import f

   We need a handler for the grouping directive. This is a class
   that implements a context decorator.  The decorator must also
   provide ``before`` and ``after`` methods that are called before
   and after any contained directives are processed.  We'll typically
   subclass ``GroupingContextDecorator``, which provides context
   decoration, and default ``before`` and ``after`` methods.

   .. doctest::

      >>> from zope.configuration.config import GroupingContextDecorator
      >>> class SampleGrouping(GroupingContextDecorator):
      ...    def before(self):
      ...       self.action(('before', self.x, self.y), f)
      ...    def after(self):
      ...       self.action(('after'), f)

   We'll use our decorator to decorate our initial context, providing
   keyword arguments x and y:

   .. doctest::

      >>> dec = SampleGrouping(context, x=1, y=2)

   Note that the keyword arguments are made attributes of the
   decorator.

   Now we'll create the stack item.

   .. doctest::

      >>> item = GroupingStackItem(dec)

   We still haven't called the before action yet, which we can verify
   by looking at the context actions:

   .. doctest::

      >>> context.actions
      []

   Subdirectives will get looked up as adapters of the context.

   We'll create a simple handler:

   .. doctest::

      >>> def simple(context, data, info):
      ...     context.action(("simple", context.x, context.y, data), f)
      ...     return info

   and register it with the context:

   .. doctest::

      >>> from zope.configuration.interfaces import IConfigurationContext
      >>> from zope.configuration.config import testns
      >>> context.register(IConfigurationContext, (testns, 'simple'), simple)

   This handler isn't really a propert handler, because it doesn't
   return a new context.  It will do for this example.

   Now we'll call the contained method on the stack item:

   .. doctest::

      >>> item.contained((testns, 'simple'), {'z': 'zope'}, "someinfo")
      'someinfo'

   We can verify thet the simple method was called by looking at the
   context actions. Note that the before method was called before
   handling the contained directive.

   .. doctest::

      >>> from pprint import PrettyPrinter
      >>> pprint = PrettyPrinter(width=60).pprint

      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': ('before', 1, 2),
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': ('simple', 1, 2, {'z': 'zope'}),
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0}]

   Finally, we call finish, which calls the decorator after method:

   .. doctest::

      >>> item.finish()

      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': ('before', 1, 2),
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': ('simple', 1, 2, {'z': 'zope'}),
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': 'after',
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0}]

   If there were no nested directives:

   .. doctest::

      >>> context = ConfigurationMachine()
      >>> dec = SampleGrouping(context, x=1, y=2)
      >>> item = GroupingStackItem(dec)
      >>> item.finish()

   Then before will be when we call finish:

   .. doctest::

      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': ('before', 1, 2),
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': 'after',
        'includepath': (),
        'info': '',
        'kw': {},
        'order': 0}]

.. autoclass:: ComplexStackItem
   :members:
   :member-order: bysource

   To see how this works, let's look at an example:

   We need a context. We'll just use a configuration machine

   .. doctest::

      >>> from zope.configuration.config import ConfigurationMachine
      >>> context = ConfigurationMachine()

   We need a callable to use in configuration actions.  We'll use a
   convenient one from the tests:

   .. doctest::

      >>> from zope.configuration.tests.directives import f

   We need a handler for the complex directive. This is a class
   with a method for each subdirective:

   .. doctest::

      >>> class Handler(object):
      ...   def __init__(self, context, x, y):
      ...      self.context, self.x, self.y = context, x, y
      ...      context.action('init', f)
      ...   def sub(self, context, a, b):
      ...      context.action(('sub', a, b), f)
      ...   def __call__(self):
      ...      self.context.action(('call', self.x, self.y), f)

   We need a complex directive definition:

   .. doctest::

      >>> from zope.interface import Interface
      >>> from zope.schema import TextLine
      >>> from zope.configuration.config import ComplexDirectiveDefinition
      >>> class Ixy(Interface):
      ...    x = TextLine()
      ...    y = TextLine()
      >>> definition = ComplexDirectiveDefinition(
      ...        context, name="test", schema=Ixy,
      ...        handler=Handler)
      >>> class Iab(Interface):
      ...    a = TextLine()
      ...    b = TextLine()
      >>> definition['sub'] = Iab, ''

   OK, now that we have the context, handler and definition, we're
   ready to use a stack item.

   .. doctest::

      >>> from zope.configuration.config import ComplexStackItem
      >>> item = ComplexStackItem(definition, context, {'x': u'xv', 'y': u'yv'},
      ...                         'foo')

   When we created the definition, the handler (factory) was called.

   .. doctest::

      >>> from pprint import PrettyPrinter
      >>> pprint = PrettyPrinter(width=60).pprint
      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': 'init',
        'includepath': (),
        'info': 'foo',
        'kw': {},
        'order': 0}]

   If a subdirective is provided, the ``contained`` method of the stack item
   is called. It will lookup the subdirective schema and call the
   corresponding method on the handler instance:

   .. doctest::

      >>> simple = item.contained(('somenamespace', 'sub'),
      ...                         {'a': u'av', 'b': u'bv'}, 'baz')
      >>> simple.finish()

   Note that the name passed to ``contained`` is a 2-part name, consisting of
   a namespace and a name within the namespace.

   .. doctest::

      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': 'init',
        'includepath': (),
        'info': 'foo',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': ('sub', u'av', u'bv'),
        'includepath': (),
        'info': 'baz',
        'kw': {},
        'order': 0}]

   The new stack item returned by contained is one that doesn't allow
   any more subdirectives,

   When all of the subdirectives have been provided, the ``finish``
   method is called:

   .. doctest::

      >>> item.finish()

   The stack item will call the handler if it is callable.

   .. doctest::

      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': 'init',
        'includepath': (),
        'info': 'foo',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': ('sub', u'av', u'bv'),
        'includepath': (),
        'info': 'baz',
        'kw': {},
        'order': 0},
       {'args': (),
        'callable': f,
        'discriminator': ('call', u'xv', u'yv'),
        'includepath': (),
        'info': 'foo',
        'kw': {},
        'order': 0}]

.. autoclass:: GroupingContextDecorator
   :members:
   :member-order: bysource

.. autoclass:: DirectiveSchema
   :members:
   :member-order: bysource

.. autointerface:: IDirectivesInfo
   :members:
   :member-order: bysource

.. autointerface:: IDirectivesContext
   :members:
   :member-order: bysource

.. autoclass:: DirectivesHandler
   :members:
   :member-order: bysource

.. autointerface:: IDirectiveInfo
   :members:
   :member-order: bysource

.. autointerface:: IFullInfo
   :members:
   :member-order: bysource

.. autointerface:: IStandaloneDirectiveInfo
   :members:
   :member-order: bysource

.. autofunction:: defineSimpleDirective

   Example:

   .. doctest::

      >>> from zope.configuration.config import ConfigurationMachine
      >>> context = ConfigurationMachine()
      >>> from zope.interface import Interface
      >>> from zope.schema import TextLine
      >>> from zope.configuration.tests.directives import f
      >>> class Ixy(Interface):
      ...    x = TextLine()
      ...    y = TextLine()
      >>> def s(context, x, y):
      ...    context.action(('s', x, y), f)

      >>> from zope.configuration.config import defineSimpleDirective
      >>> defineSimpleDirective(context, 's', Ixy, s, testns)

      >>> context((testns, "s"), x=u"vx", y=u"vy")
      >>> from pprint import PrettyPrinter
      >>> pprint = PrettyPrinter(width=60).pprint
      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': ('s', u'vx', u'vy'),
        'includepath': (),
        'info': None,
        'kw': {},
        'order': 0}]

      >>> context(('http://www.zope.com/t1', "s"), x=u"vx", y=u"vy")
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Unknown directive', 'http://www.zope.com/t1', 's')

      >>> context = ConfigurationMachine()
      >>> defineSimpleDirective(context, 's', Ixy, s, "*")

      >>> context(('http://www.zope.com/t1', "s"), x=u"vx", y=u"vy")
      >>> pprint(context.actions)
      [{'args': (),
        'callable': f,
        'discriminator': ('s', u'vx', u'vy'),
        'includepath': (),
        'info': None,
        'kw': {},
        'order': 0}]

.. autofunction:: defineGroupingDirective

   Example:

   .. doctest::

      >>> from zope.configuration.config import ConfigurationMachine
      >>> context = ConfigurationMachine()
      >>> from zope.interface import Interface
      >>> from zope.schema import TextLine
      >>> from zope.configuration.tests.directives import f
      >>> class Ixy(Interface):
      ...    x = TextLine()
      ...    y = TextLine()

   We won't bother creating a special grouping directive class. We'll
   just use :class:`GroupingContextDecorator`, which simply sets up a
   grouping context that has extra attributes defined by a schema:

   .. doctest::

      >>> from zope.configuration.config import defineGroupingDirective
      >>> from zope.configuration.config import GroupingContextDecorator
      >>> defineGroupingDirective(context, 'g', Ixy,
      ...                         GroupingContextDecorator, testns)

      >>> context.begin((testns, "g"), x=u"vx", y=u"vy")
      >>> context.stack[-1].context.x
      u'vx'
      >>> context.stack[-1].context.y
      u'vy'

      >>> context(('http://www.zope.com/t1', "g"), x=u"vx", y=u"vy")
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Unknown directive', 'http://www.zope.com/t1', 'g')

      >>> context = ConfigurationMachine()
      >>> defineGroupingDirective(context, 'g', Ixy,
      ...                         GroupingContextDecorator, "*")

      >>> context.begin(('http://www.zope.com/t1', "g"), x=u"vx", y=u"vy")
      >>> context.stack[-1].context.x
      u'vx'
      >>> context.stack[-1].context.y
      u'vy'

.. autointerface:: IComplexDirectiveContext
   :members:
   :member-order: bysource

.. autoclass:: ComplexDirectiveDefinition
   :members:
   :member-order: bysource

.. autofunction:: subdirective

.. autointerface:: IProvidesDirectiveInfo
   :members:
   :member-order: bysource

.. autofunction:: provides

   Example:

   .. doctest::

      >>> from zope.configuration.config import ConfigurationContext
      >>> from zope.configuration.config import provides
      >>> c = ConfigurationContext()
      >>> provides(c, 'apidoc')
      >>> c.hasFeature('apidoc')
      True

   Spaces are not allowed in feature names (this is reserved for providing
   many features with a single directive in the futute).

   .. doctest::

      >>> provides(c, 'apidoc onlinehelp')
      Traceback (most recent call last):
        ...
      ValueError: Only one feature name allowed

      >>> c.hasFeature('apidoc onlinehelp')
      False

.. autofunction:: toargs

   Example:

   .. doctest::

      >>> from zope.configuration.config import toargs
      >>> from zope.schema import BytesLine
      >>> from zope.schema import Float
      >>> from zope.schema import Int
      >>> from zope.schema import TextLine
      >>> from zope.schema import URI
      >>> class schema(Interface):
      ...     in_ = Int(constraint=lambda v: v > 0)
      ...     f = Float()
      ...     n = TextLine(min_length=1, default=u"rob")
      ...     x = BytesLine(required=False)
      ...     u = URI()

      >>> context = ConfigurationMachine()
      >>> from pprint import PrettyPrinter
      >>> pprint=PrettyPrinter(width=50).pprint

      >>> pprint(toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2', 'n': u'bob', 'x': u'x.y.z',
      ...          'u': u'http://www.zope.org' }))
      {'f': 1.2,
       'in_': 1,
       'n': u'bob',
       'u': 'http://www.zope.org',
       'x': 'x.y.z'}

   If we have extra data, we'll get an error:

   .. doctest::

      >>> toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2', 'n': u'bob', 'x': u'x.y.z',
      ...          'u': u'http://www.zope.org', 'a': u'1'})
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Unrecognized parameters:', 'a')

   Unless we set a tagged value to say that extra arguments are ok:

   .. doctest::

      >>> schema.setTaggedValue('keyword_arguments', True)

      >>> pprint(toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2', 'n': u'bob', 'x': u'x.y.z',
      ...          'u': u'http://www.zope.org', 'a': u'1'}))
      {'a': u'1',
       'f': 1.2,
       'in_': 1,
       'n': u'bob',
       'u': 'http://www.zope.org',
       'x': 'x.y.z'}

   If we omit required data we get an error telling us what was omitted:

   .. doctest::

      >>> pprint(toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2', 'n': u'bob', 'x': u'x.y.z'}))
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Missing parameter:', 'u')

   Although we can omit not-required data:

   .. doctest::

      >>> pprint(toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2', 'n': u'bob',
      ...          'u': u'http://www.zope.org', 'a': u'1'}))
      {'a': u'1',
       'f': 1.2,
       'in_': 1,
       'n': u'bob',
       'u': 'http://www.zope.org'}

   And we can omit required fields if they have valid defaults
   (defaults that are valid values):

   .. doctest::

      >>> pprint(toargs(context, schema,
      ...        {'in': u'1', 'f': u'1.2',
      ...          'u': u'http://www.zope.org', 'a': u'1'}))
      {'a': u'1',
       'f': 1.2,
       'in_': 1,
       'n': u'rob',
       'u': 'http://www.zope.org'}

   We also get an error if any data was invalid:

   .. doctest::

      >>> pprint(toargs(context, schema,
      ...        {'in': u'0', 'f': u'1.2', 'n': u'bob', 'x': u'x.y.z',
      ...          'u': u'http://www.zope.org', 'a': u'1'}))
      Traceback (most recent call last):
      ...
      ConfigurationError: ('Invalid value for', 'in', '0')

.. autofunction:: expand_action

.. autofunction:: resolveConflicts

.. autoclass:: ConfigurationConflictError
