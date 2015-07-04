================
Around the Globe
================
------------------------
A small timezone utility
------------------------

.. image:: https://api.travis-ci.org/crodjer/atg.svg
.. image:: https://coveralls.io/repos/crodjer/atg/badge.svg?branch=master

.. code ::

    $ atg Mountain View
    Their timezone is "America/Los_Angeles"
    Their time: Sat Jul  4 07:13:34 2015
    People there may be sleeping.
    Convenient time slots:
        08:00 to 11:00 here i.e. 19:30 to 22:30 there
        20:30 to 22:30 here i.e. 08:00 to 10:00 there

Features
--------

 - Get the timezone for a random address.
 - Current time anywhere.
 - Guesses about what people may be doing.
 - Helps you schedule meetings by providing you spans of convenient times.

Installation
------------

This is a Python package, which can be simply installed through pip:

.. code :: sh

   # $HOME/.local/bin should be in $PATH for this to work.
   $ pip install --user atg


and to install it globall, run:


.. code :: sh

   $ sudo pip install atg


Usage
-----

Get all the information about the time at **Mountain View**:

.. code ::

    $ atg Mountain View
    Their timezone is "America/Los_Angeles"
    Their time: Sat Jul  4 07:13:34 2015
    People there may be sleeping.
    Convenient time slots:
        08:00 to 11:00 here i.e. 19:30 to 22:30 there
        20:30 to 22:30 here i.e. 08:00 to 10:00 there


By default, ``atg`` calculates time slots based to avoid sleep periods. You can
use ``--dnd`` to customize this. For example, to avoid disturbing at work/sleep:

.. code ::

    $ atg Mountain View --dnd work --dnd sleep

You can also specify who the timeslots should be convenient to. By default it
will consider both. If you want the convenient timings for the remote location:

.. code ::

    $ atg Mountain View -c there


You may also use the flag ``--convenient-for`` flag. If you don't care about the
remote location's convenience:

.. code ::

    $ atg Mountain View --convenient-for here


Help
====

You can always refer to the command usage through ``atg -h``.

.. code ::

    usage: atg [-h] [--dnd {work,sleep,available}] [-c {here,there}]
               [-m MY_LOCATION] [-x {timezone,now,default,status,schedule}]
               remote [remote ...]

    positional arguments:
      remote                the remote location

    optional arguments:
      -h, --help            show this help message and exit
      --dnd {work,sleep,available}
                            the do not disturb activities (default: sleep)
      -c {here,there}, --convenient-for {here,there}
                            which side's convenience should be considered
                            (default: both)
      -m MY_LOCATION, --my-location MY_LOCATION
                            specify your own location (default from system time)
      -x {timezone,now,default,status,schedule}, --command {timezone,now,default,status,schedule}
                            the command for atg to execute



Developing and Testing
======================

``atg`` uses the pytz_, tzlocal_ and enum34_ (for backwards compatibility) as dependencies.

To set things up for development, create and activate a virtualenv_ and run


.. code ::

    $ pip install -e .[dev,test]
    $ python setup.py develop

Tests
-----

Tests and CI integration is still being worked on. To run tests, execute:

.. code ::

    $ nosetests


Bugs
----

Probably lots. Please send us reports on the Github `issue tracker <https://github.com/crodjer/atz/issues>`_. Patches are welcome too.

.. _pytz: https://pypi.python.org/pypi/pytz
.. _tzlocal: https://pypi.python.org/pypi/tzlocal
.. _enum34: https://pypi.python.org/pypi/enum34
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
