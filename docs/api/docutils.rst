:mod:`zope.configuration.docutils`
==================================

.. module:: zope.configuration.docutils

.. autofunction:: wrap

   Examples:

   .. doctest::

      >>> from zope.configuration.docutils import wrap
      >>> print wrap('foo bar')[:-2]
      foo bar
      >>> print wrap('foo bar', indent=2)[:-2]
        foo bar
      >>> print wrap('foo bar, more foo bar', 10)[:-2]
      foo bar,
      more foo
      bar
      >>> print wrap('foo bar, more foo bar', 10, 2)[:-2]
        foo bar,
        more foo
        bar

.. autofunction:: makeDocStructures
