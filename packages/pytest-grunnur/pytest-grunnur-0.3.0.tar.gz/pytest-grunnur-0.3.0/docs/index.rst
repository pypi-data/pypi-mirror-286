.. grunnur documentation master file, created by
   sphinx-quickstart on Tue Jan 28 16:50:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A ``py.test`` plugin for ``grunnur``
====================================

This package contains a collection of helpers useful for testing ``grunnur``-based libraries and applications.
See `the Grunnur docs <https://grunnur.readthedocs.io/>`_ for more details about the main package.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Public API
==========

.. currentmodule:: pytest_grunnur


Py.Test hooks
-------------

These are invoked automatically if you use ``pytest_grunnur`` as a ``py.test`` plugin.

.. autofunction:: pytest_grunnur.plugin.pytest_addoption

.. autofunction:: pytest_grunnur.plugin.pytest_report_header

.. autofunction:: pytest_grunnur.plugin.pytest_generate_tests


Fixtures
--------

.. autofunction:: pytest_grunnur.plugin.api

.. autofunction:: pytest_grunnur.plugin.platform

.. autofunction:: pytest_grunnur.plugin.device

.. autofunction:: pytest_grunnur.plugin.context

.. autofunction:: pytest_grunnur.plugin.some_device

.. autofunction:: pytest_grunnur.plugin.some_context

.. autofunction:: pytest_grunnur.plugin.multi_device_set

.. autofunction:: pytest_grunnur.plugin.multi_device_context


Utility functions
-----------------

.. autofunction:: get_apis

.. autofunction:: get_platforms

.. autofunction:: get_devices

.. autofunction:: get_multi_device_sets


Version history
===============


0.3.0 (25 Jul 2024)
-------------------

Changed
^^^^^^^

- Bumped Python version to 3.10. (PR_1_)


.. _PR_1: https://github.com/fjarri/pytest-grunnur/pull/1


0.2.1 (5 Feb 2023)
------------------

Fixed
^^^^^

- Switched back to static versioning.


0.2.0 (4 Feb 2023)
------------------

All the fixtures are now explicitly defined.


0.1.0 (29 Jan 2023)
-------------------

Initial version
