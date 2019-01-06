=============
Border-Patrol
=============

Border-Patrol logs all imported packages and their version to support you while debugging. In 95% of all cases when
something suddenly breaks in production it is due to some different version in one of your requirements. Pinning down the
versions of all your dependencies and dependencies of dependencies inside a virtual environments helps you to overcome
this problem but is quite cumbersome and thus this method is not always applied in practice. Also sometimes, like when
you are using PySpark, you might not be 100% sure which library versions are installed on some cluster nodes.

With Border-Patrol you can easily find the culprit by looking in the logs of the last working versions and compare it
to the failing one since Border-Patrol will list all imported packages and their corresponding version right at the
end of your application, even if it crashed.

Usage
=====

Border-Patrol is really simple to use, just install it with ``pip install border-patrol``
and import it before any other package, e.g.::

    from border_patrol import with_print_stdout

    import pandas as pd

If you run those lines in a script, you will get a similar output to this one::

    Python version is 3.6.7 |Anaconda, Inc.| (default, Oct 23 2018, 14:01:38)
    [GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)]
    Following packages were imported:
    PACKAGE         VERSION   PATH
    border_patrol   0.1       /Users/fwilhelm/Sources/border_patrol/src/border_patrol
    cycler          0.10.0    /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/cycler.py
    dateutil        2.7.5     /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/dateutil/__init__.py
    matplotlib      2.2.3     /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/matplotlib/__init__.py
    numpy           1.15.1    /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/numpy/__init__.py
    pandas          0.23.4    /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/pandas/__init__.py
    pyparsing       2.3.0     /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/pyparsing.py
    pytz            2018.7    /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/pytz/__init__.py
    six             1.11.0    /Users/fwilhelm/anaconda/envs/lib/python3.6/site-packages/six.py

If you import ``with_print_stdout``, Border-Patrol will use ``print`` as output function whereas ``with_print_stderr`` will
print to standard error. Since most production applications will rather use the ``logging`` module, you can tell
Border-Patrol to use it by importing ``with_log_{error|warning|info|debug}``.
For instance ``from border_patrol import with_log_info`` will log the final report by using the ``INFO`` logging level.

If you want even more fine grained control you can import the ``BorderPatrol`` class directly from the ``border_patrol`` package
and use the ``register()`` and ``unregister()`` method to activate and deactivate it, respectively. At any point the
tracking can be circumvented by using ``border_patrol.builtin_import``.


How does it work?
=================

Border-Patrol is actually quite simple. It overwrites the ``__import__`` function in Python's ``builtins`` package to track
every imported module. For each module the corresponding package is determined and the version number is retrieved with
the help of the ``__version__`` attribute which most professional libraries provide at the package level. If this fails
the distribution name for the package is determined, e.g. ``scikit-learn`` is the distribution containing the ``sklearn`` package,
with the help of ``pkg_resources`` which is a part of ``setuptools``. Then the distribution name is used to determine the
version number also using ``pkg_resources`` similar to how ``pip`` would do it.

Finally, Border-Patrol registers an ``atexit`` handler to be called when your application finishes and
reports all imported modules. To avoid any problem registering these things more than once, Border-Patrol is implemented
as a singleton and thus it is *not* thread-safe.


Note
====

This project has been set up using PyScaffold 3.1. For details and usage information on PyScaffold see https://pyscaffold.org/.


Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
