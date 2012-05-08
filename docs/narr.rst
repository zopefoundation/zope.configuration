==========================
Zope configuration system
==========================

The zope configuration system provides an extensible system for
supporting variouse kinds of configurations.

It is based on the idea of configuration directives. Users of the
configuration system provide configuration directives in some
language that express configuration choices. The intent is that the
language be pluggable.  An XML language is provided by default.

Configuration is performed in three stages. In the first stage,
directives are processed to compute configuration actions.
Configuration actions consist of:

- A discriminator

- A callable

- Positional arguments

- Keyword arguments

The actions are essentially delayed function calls.  Two or more
actions conflict if they have the same discriminator.  The
configuration system has rules for resolving conflicts. If conflicts
cannot be resolved, an error will result.  Conflict resolution
typically discards all but one of the conflicting actions, so that
the remaining action of the originally-conflicting actions no longer
conflicts.  Non-conflicting actions are executed in the order that
they were created by passing the positional and non-positional
arguments to the action callable.

The system is extensible. There is a meta-configuration language for
defining configuration directives. A directive is defined by
providing meta data about the directive and handler code to process
the directive.  There are four kinds of directives:

- Simple directives compute configuration actions.  Their handlers
  are typically functions that take a context and zero or more
  keyword arguments and return a sequence of configuration actions.

  To learn how to create simple directives, see `tests/test_simple.py`.


- Grouping directives collect information to be used by nested
  directives. They are called with a context object which they adapt
  to some interface that extends IConfigurationContext.

  To learn how to create grouping directives, look at the
  documentation in zopeconfigure.py, which provides the implementation
  of the zope `configure` directive.

  Other directives can be nested in grouping directives.

  To learn how to implement nested directives, look at the
  documentation in `tests/test_nested.py`.

- Complex directives are directives that have subdirectives.  
  Subdirectives have handlers that are simply methods of complex
  directives. Complex diretives are handled by factories, typically
  classes, that create objects that have methods for handling
  subdirectives. These objects also have __call__ methods that are
  called when processing of subdirectives is finished.

  Complex directives only exist to support old directive
  handlers. They will probably be deprecated in the future.

- Subdirectives are nested in complex directives. They are like
  simple directives except that they hane handlers that are complex
  directive methods.

  Subdirectives, like complex directives only exist to support old
  directive handlers. They will probably be deprecated in the future.

.. todo::
   Flesh out narrative docs.
    
Using the configuration machinery programattically
==================================================

An extended example:

.. doctest::

   >>> from zope.configuration.config import ConfigurationMachine
   >>> from zope.configuration.config import metans
   >>> machine = ConfigurationMachine()
   >>> ns = "http://www.zope.org/testing"

Register some test directives:

Start with a grouping directive that sets a package:

.. doctest::

   >>> machine((metans, "groupingDirective"),
   ...         name="package", namespace=ns,
   ...         schema="zope.configuration.tests.directives.IPackaged",
   ...         handler="zope.configuration.tests.directives.Packaged",
   ...         )

Now we can set the package:

.. doctest::

   >>> machine.begin((ns, "package"),
   ...               package="zope.configuration.tests.directives",
   ...               )

Which makes it easier to define the other directives:

First, define some simple directives:

.. doctest::

   >>> machine((metans, "directive"),
   ...         namespace=ns, name="simple",
   ...         schema=".ISimple", handler=".simple")

   >>> machine((metans, "directive"),
   ...         namespace=ns, name="newsimple",
   ...         schema=".ISimple", handler=".newsimple")


and try them out:

.. doctest::

   >>> machine((ns, "simple"), "first", a=u"aa", c=u"cc")
   >>> machine((ns, "newsimple"), "second", a=u"naa", c=u"ncc", b=u"nbb")

   >>> from pprint import PrettyPrinter
   >>> pprint = PrettyPrinter(width=50).pprint

   >>> pprint(machine.actions)
   [{'args': (u'aa', u'xxx', 'cc'),
     'callable': f,
     'discriminator': ('simple',
                       u'aa',
                       u'xxx',
                       'cc'),
     'includepath': (),
     'info': 'first',
     'kw': {},
     'order': 0},
    {'args': (u'naa', u'nbb', 'ncc'),
     'callable': f,
     'discriminator': ('newsimple',
                       u'naa',
                       u'nbb',
                       'ncc'),
     'includepath': (),
     'info': 'second',
     'kw': {},
     'order': 0}]

Define and try a simple directive that uses a component:

.. doctest::

   >>> machine((metans, "directive"),
   ...         namespace=ns, name="factory",
   ...         schema=".IFactory", handler=".factory")


   >>> machine((ns, "factory"), factory=u".f")
   >>> pprint(machine.actions[-1:])
   [{'args': (),
     'callable': f,
     'discriminator': ('factory', 1, 2),
     'includepath': (),
     'info': None,
     'kw': {},
     'order': 0}]

Define and try a complex directive:

.. doctest::

   >>> machine.begin((metans, "complexDirective"),
   ...               namespace=ns, name="testc",
   ...               schema=".ISimple", handler=".Complex")

   >>> machine((metans, "subdirective"),
   ...         name="factory", schema=".IFactory")

   >>> machine.end()

   >>> machine.begin((ns, "testc"), None, "third", a=u'ca', c='cc')
   >>> machine((ns, "factory"), "fourth", factory=".f")

Note that we can't call a complex method unless there is a directive for
it:

.. doctest::

   >>> machine((ns, "factory2"), factory=".f")
   Traceback (most recent call last):
   ...
   ConfigurationError: ('Invalid directive', 'factory2')


   >>> machine.end()
   >>> pprint(machine.actions)
   [{'args': (u'aa', u'xxx', 'cc'),
     'callable': f,
     'discriminator': ('simple',
                       u'aa',
                       u'xxx',
                       'cc'),
     'includepath': (),
     'info': 'first',
     'kw': {},
     'order': 0},
    {'args': (u'naa', u'nbb', 'ncc'),
     'callable': f,
     'discriminator': ('newsimple',
                       u'naa',
                       u'nbb',
                       'ncc'),
     'includepath': (),
     'info': 'second',
     'kw': {},
     'order': 0},
    {'args': (),
     'callable': f,
     'discriminator': ('factory', 1, 2),
     'includepath': (),
     'info': None,
     'kw': {},
     'order': 0},
    {'args': (),
     'callable': None,
     'discriminator': 'Complex.__init__',
     'includepath': (),
     'info': 'third',
     'kw': {},
     'order': 0},
    {'args': (u'ca',),
     'callable': f,
     'discriminator': ('Complex.factory', 1, 2),
     'includepath': (),
     'info': 'fourth',
     'kw': {},
     'order': 0},
    {'args': (u'xxx', 'cc'),
     'callable': f,
     'discriminator': ('Complex', 1, 2),
     'includepath': (),
     'info': 'third',
     'kw': {},
     'order': 0}]

Done with the package

.. doctest::

   >>> machine.end()


Verify that we can use a simple directive outside of the package:

.. doctest::

   >>> machine((ns, "simple"), a=u"oaa", c=u"occ", b=u"obb")

But we can't use the factory directive, because it's only valid
inside a package directive:

.. doctest::

   >>> machine((ns, "factory"), factory=u".F")
   Traceback (most recent call last):
   ...
   ConfigurationError: ('Invalid value for', 'factory',""" \
      """ "Can't use leading dots in dotted names, no package has been set.")

   >>> pprint(machine.actions)
   [{'args': (u'aa', u'xxx', 'cc'),
     'callable': f,
     'discriminator': ('simple',
                       u'aa',
                       u'xxx',
                       'cc'),
     'includepath': (),
     'info': 'first',
     'kw': {},
     'order': 0},
    {'args': (u'naa', u'nbb', 'ncc'),
     'callable': f,
     'discriminator': ('newsimple',
                       u'naa',
                       u'nbb',
                       'ncc'),
     'includepath': (),
     'info': 'second',
     'kw': {},
     'order': 0},
    {'args': (),
     'callable': f,
     'discriminator': ('factory', 1, 2),
     'includepath': (),
     'info': None,
     'kw': {},
     'order': 0},
    {'args': (),
     'callable': None,
     'discriminator': 'Complex.__init__',
     'includepath': (),
     'info': 'third',
     'kw': {},
     'order': 0},
    {'args': (u'ca',),
     'callable': f,
     'discriminator': ('Complex.factory', 1, 2),
     'includepath': (),
     'info': 'fourth',
     'kw': {},
     'order': 0},
    {'args': (u'xxx', 'cc'),
     'callable': f,
     'discriminator': ('Complex', 1, 2),
     'includepath': (),
     'info': 'third',
     'kw': {},
     'order': 0},
    {'args': (u'oaa', u'obb', 'occ'),
     'callable': f,
     'discriminator': ('simple',
                       u'oaa',
                       u'obb',
                       'occ'),
     'includepath': (),
     'info': None,
     'kw': {},
     'order': 0}]


Overriding Included Configuration
==================================

When we have conflicting directives, we can resolve them if one of
the conflicting directives was from a file that included all of
the others.  The problem with this is that this requires that all
of the overriding directives be in one file, typically the
top-most including file. This isn't very convenient.  Fortunately,
we can overcome this with the includeOverrides directive. Let's
look at an example to see how this works.

Look at the file ``bar.zcml`` (in ``zope/configuration/tests/samplepackage``):

- It includes ``bar1.zcml`` and ``bar2.zcml``.

- ``bar1.zcml`` includes ``configure.zcml`` and has a ``foo``
  directive.
  
- ``bar2.zcml`` includes ``bar21.zcml``, and has a ``foo``
  directive that conflicts with one in ``bar1.zcml``.
  
- ``bar2.zcml`` also overrides a foo directive in ``bar21.zcml``.

- ``bar21.zcml`` has a ``foo`` directive that conflicts with one in in
  ``configure.zcml``. Whew!

Let's see what happens when we try to process ``bar.zcml``.

.. doctest::

   >>> import os
   >>> from zope.configuration.config import ConfigurationMachine
   >>> from zope.configuration.xmlconfig import include
   >>> from zope.configuration.xmlconfig import registerCommonDirectives
   >>> context = ConfigurationMachine()
   >>> registerCommonDirectives(context)

   >>> from zope.configuration.tests import __file__
   >>> here = os.path.dirname(__file__)
   >>> path = os.path.join(here, "samplepackage", "bar.zcml")
   >>> include(context, path)

So far so good, let's look at the configuration actions:

.. doctest::

   >>> from zope.configuration.tests.test_xmlconfig import clean_actions
   >>> pprint = PrettyPrinter(width=70).pprint
   >>> pprint(clean_actions(context.actions))
   [{'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar1.zcml',
                     'tests/samplepackage/configure.zcml'],
     'info': 'File "tests/samplepackage/configure.zcml", line 12.2-12.29'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar1.zcml'],
     'info': 'File "tests/samplepackage/bar1.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar2.zcml',
                     'tests/samplepackage/bar21.zcml'],
     'info': 'File "tests/samplepackage/bar21.zcml", line 3.2-3.24'},
    {'discriminator': (('x', 'blah'), ('y', 2)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar2.zcml',
                     'tests/samplepackage/bar21.zcml'],
     'info': 'File "tests/samplepackage/bar21.zcml", line 4.2-4.24'},
    {'discriminator': (('x', 'blah'), ('y', 2)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar2.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/bar.zcml',
                     'tests/samplepackage/bar2.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 6.2-6.24'}]

As you can see, there are a number of conflicts (actions with the same
discriminator).  Some of these can be resolved, but many can't, as
we'll find if we try to execuse the actions:

.. doctest::

   >>> from zope.configuration.config import ConfigurationConflictError
   >>> from zope.configuration.tests.test_xmlconfig import clean_text_w_paths
   >>> try:
   ...    v = context.execute_actions()
   ... except ConfigurationConflictError, v:
   ...    pass
   >>> print clean_text_w_paths(str(v))
   Conflicting configuration actions
     For: (('x', 'blah'), ('y', 0))
       File "tests/samplepackage/configure.zcml", line 12.2-12.29
           <test:foo x="blah" y="0" />
       File "tests/samplepackage/bar21.zcml", line 3.2-3.24
           <foo x="blah" y="0" />
     For: (('x', 'blah'), ('y', 1))
       File "tests/samplepackage/bar1.zcml", line 5.2-5.24
           <foo x="blah" y="1" />
       File "tests/samplepackage/bar2.zcml", line 6.2-6.24
           <foo x="blah" y="1" />

Note that the conflicts for (('x', 'blah'), ('y', 2)) aren't
included in the error because they could be resolved.

Let's try this again using includeOverrides.  We'll include
baro.zcml which includes bar2.zcml as overrides.

.. doctest::

   >>> context = ConfigurationMachine()
   >>> registerCommonDirectives(context)
   >>> path = os.path.join(here, "samplepackage", "baro.zcml")
   >>> include(context, path)

Now, if we look at the actions:

.. doctest::

   >>> pprint(clean_actions(context.actions))
   [{'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/baro.zcml',
                     'tests/samplepackage/bar1.zcml',
                     'tests/samplepackage/configure.zcml'],
     'info': 'File "tests/samplepackage/configure.zcml", line 12.2-12.29'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/baro.zcml',
                     'tests/samplepackage/bar1.zcml'],
     'info': 'File "tests/samplepackage/bar1.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/baro.zcml'],
     'info': 'File "tests/samplepackage/bar21.zcml", line 3.2-3.24'},
    {'discriminator': (('x', 'blah'), ('y', 2)),
     'includepath': ['tests/samplepackage/baro.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/baro.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 6.2-6.24'}]

We see that:

- The conflicting actions between bar2.zcml and bar21.zcml have
  been resolved, and

- The remaining (after conflict resolution) actions from bar2.zcml
  and bar21.zcml have the includepath that they would have if they
  were defined in baro.zcml and this override the actions from
  bar1.zcml and configure.zcml.

We can now execute the actions without problem, since the
remaining conflicts are resolvable:

.. doctest::

   >>> context.execute_actions()

We should now have three entries in foo.data:

.. doctest::

   >>> from zope.configuration.tests.samplepackage import foo
   >>> from zope.configuration.tests.test_xmlconfig import clean_info_path
   >>> len(foo.data)
   3

   >>> data = foo.data.pop(0)
   >>> data.args
   (('x', 'blah'), ('y', 0))
   >>> print clean_info_path(`data.info`)
   File "tests/samplepackage/bar21.zcml", line 3.2-3.24

   >>> data = foo.data.pop(0)
   >>> data.args
   (('x', 'blah'), ('y', 2))
   >>> print clean_info_path(`data.info`)
   File "tests/samplepackage/bar2.zcml", line 5.2-5.24

   >>> data = foo.data.pop(0)
   >>> data.args
   (('x', 'blah'), ('y', 1))
   >>> print clean_info_path(`data.info`)
   File "tests/samplepackage/bar2.zcml", line 6.2-6.24


We expect the exact same results when using includeOverrides with
the ``files`` argument instead of the ``file`` argument.  The
baro2.zcml file uses the former:

.. doctest::

   >>> context = ConfigurationMachine()
   >>> registerCommonDirectives(context)
   >>> path = os.path.join(here, "samplepackage", "baro2.zcml")
   >>> include(context, path)

Actions look like above:

.. doctest::

   >>> pprint(clean_actions(context.actions))
   [{'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/baro2.zcml',
                     'tests/samplepackage/bar1.zcml',
                     'tests/samplepackage/configure.zcml'],
     'info': 'File "tests/samplepackage/configure.zcml", line 12.2-12.29'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/baro2.zcml',
                     'tests/samplepackage/bar1.zcml'],
     'info': 'File "tests/samplepackage/bar1.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 0)),
     'includepath': ['tests/samplepackage/baro2.zcml'],
     'info': 'File "tests/samplepackage/bar21.zcml", line 3.2-3.24'},
    {'discriminator': (('x', 'blah'), ('y', 2)),
     'includepath': ['tests/samplepackage/baro2.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 5.2-5.24'},
    {'discriminator': (('x', 'blah'), ('y', 1)),
     'includepath': ['tests/samplepackage/baro2.zcml'],
     'info': 'File "tests/samplepackage/bar2.zcml", line 6.2-6.24'}]

   >>> context.execute_actions()
   >>> len(foo.data)
   3
   >>> del foo.data[:]



Making specific directives conditional
======================================

There is a ``condition`` attribute in the
"http://namespaces.zope.org/zcml" namespace which is honored on all
elements in ZCML.  The value of the attribute is an expression
which is used to determine if that element and its descendents are
used.  If the condition is true, processing continues normally,
otherwise that element and its descendents are ignored.

Currently the expression is always of the form "have featurename", and it
checks for the presence of a ``<meta:provides feature="featurename" />``.

Our demonstration uses a trivial registry; each registration consists
of a simple id inserted in the global `registry` in this module.  We
can checked that a registration was made by checking whether the id is
present in `registry`.

.. doctest::

   >>> from zope.configuration.tests.conditions import registry
   >>> registry
   []

We start by loading the example ZCML file, *conditions.zcml*:

.. doctest::

  >>> import zope.configuration.tests
  >>> from zope.configuration.xmlconfig import file
  >>> context = file("conditions.zcml", zope.configuration.tests)

To show that our sample directive works, we see that the unqualified
registration was successful:

.. doctest::

  >>> "unqualified.registration" in registry
  True

When the expression specified with ``zcml:condition`` evaluates to
true, the element it is attached to and all contained elements (not
otherwise conditioned) should be processed normally:

.. doctest::

  >>> "direct.true.condition" in registry
  True
  >>> "nested.true.condition" in registry
  True

However, when the expression evaluates to false, the conditioned
element and all contained elements should be ignored:

.. doctest::

  >>> "direct.false.condition" in registry
  False
  >>> "nested.false.condition" in registry
  False

Conditions on container elements affect the conditions in nested
elements in a reasonable way.  If an "outer" condition is true, nested
conditions are processed normally:

.. doctest::

  >>> "true.condition.nested.in.true" in registry
  True
  >>> "false.condition.nested.in.true" in registry
  False

If the outer condition is false, inner conditions are not even
evaluated, and the nested elements are ignored:

.. doctest::

  >>> "true.condition.nested.in.false" in registry
  False
  >>> "false.condition.nested.in.false" in registry
  False

.. testcleanup::

  del registry[:]


Filtering and Inhibiting Configuration
======================================

The ``exclude`` standard directive is provided for inhibiting unwanted
configuration. It is used to exclude processing of configuration files.
It is useful when including a configuration that includes some other
configuration that you don't want.

It must be used BEFORE including the files to be excluded.

First, let's look at an example.  The zope.configuration.tests.excludedemo
package has a ZCML configuration that includes some other configuration files.

We'll set a log handler so we can see what's going on:

.. doctest::

   >>> import logging
   >>> import logging.handlers
   >>> import sys
   >>> logger = logging.getLogger('config')
   >>> oldlevel = logger.level
   >>> logger.setLevel(logging.DEBUG)
   >>> handler = logging.handlers.MemoryHandler(10)
   >>> logger.addHandler(handler)
 
Now, we'll include the zope.configuration.tests.excludedemo config:

.. doctest::

   >>> from zope.configuration.xmlconfig import string
   >>> _ = string('<include package="zope.configuration.tests.excludedemo" />')
   >>> len(handler.buffer)
   3
   >>> logged = [x.msg for x in handler.buffer]
   >>> logged[0].startswith('include ')
   True
   >>> logged[0].endswith('src/zope/configuration/tests/excludedemo/configure.zcml')
   True
   >>> logged[1].startswith('include ')
   True
   >>> logged[1].endswith('src/zope/configuration/tests/excludedemo/sub/configure.zcml')
   True
   >>> logged[2].startswith('include ')
   True
   >>> logged[2].endswith('src/zope/configuration/tests/excludedemo/spam.zcml')
   True
   >>> del handler.buffer[:]

Each run of the configuration machinery runs with fresh state, so
rerunning gives the same thing:

.. doctest::

   >>> _ = string('<include package="zope.configuration.tests.excludedemo" />')
   >>> len(handler.buffer)
   3
   >>> logged = [x.msg for x in handler.buffer]
   >>> logged[0].startswith('include ')
   True
   >>> logged[0].endswith('src/zope/configuration/tests/excludedemo/configure.zcml')
   True
   >>> logged[1].startswith('include ')
   True
   >>> logged[1].endswith('src/zope/configuration/tests/excludedemo/sub/configure.zcml')
   True
   >>> logged[2].startswith('include ')
   True
   >>> logged[2].endswith('src/zope/configuration/tests/excludedemo/spam.zcml')
   True
   >>> del handler.buffer[:]

Now, we'll use the exclude directive to exclude the two files included
by the configuration file in zope.configuration.tests.excludedemo:

.. doctest::

   >>> _ = string(
   ... '''
   ... <configure  xmlns="http://namespaces.zope.org/zope">
   ...   <exclude package="zope.configuration.tests.excludedemo.sub" />
   ...   <exclude package="zope.configuration.tests.excludedemo" file="spam.zcml" />
   ...   <include package="zope.configuration.tests.excludedemo" />
   ... </configure>
   ... ''')
   >>> len(handler.buffer)
   1
   >>> logged = [x.msg for x in handler.buffer]
   >>> logged[0].startswith('include ')
   True
   >>> logged[0].endswith('src/zope/configuration/tests/excludedemo/configure.zcml')
   True


.. testcleanup::

   logger.setLevel(oldlevel)
   logger.removeHandler(handler)
