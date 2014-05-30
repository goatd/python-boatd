============
python-goatd
============

.. image:: https://pypip.in/v/goatd_client/badge.png
    :target: https://pypi.python.org/pypi/goatd_client
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/goatd/python-goatd.png?branch=master
    :target: https://travis-ci.org/goatd/python-goatd

Python module for writing `goatd <https://github.com/goatd/goatd>`_ behavior
scripts.

Installing
==========

``$ pip install goatd_client``

class **Goat**
==============

A goat controlled by goatd


**Attributes**
----------------

``heading``:
Return the current heading of the goat in degrees

``position``:
Return a tuple in the form ``(latitude, longitude)``

``version``:
Return the version of goatd

``wind``:
Return the direction of the wind in degrees

**methods**
-----------

``def __init__(self, host='localhost', port=2222)``

Create a goat instance, connecting to goatd at ``host`` on port ``port``

``def __rudder__(self, angle)``

Set the angle of the rudder to be ``angle`` degrees

``def __sail__(self, angle)``

Set the angle of the sail to ``angle`` degrees

