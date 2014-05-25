python-goatd
============

[![BuildStatus](https://travis-ci.org/goatd/python-goatd.png?branch=master)](https://travis-ci.org/goatd/python-goatd)

Python module for writing [goatd](https://github.com/goatd/goatd) behavior
scripts.

## class __Goat__
****************************************
A goat controlled by goatd


### __descriptors__
****************************************
#### __heading__
Return the current heading of the goat in degrees

#### __position__
Return a tuple in the form `(latitude, longitude)`

#### __version__
Return the version of goatd

#### __wind__
Return the direction of the wind in degrees

### __methods__
****************************************
#### def __\__init__\__(self, host='localhost', port=2222):

Create a goat instance, connecting to goatd at `host` on port `port`

#### def __rudder__(self, angle):

Set the angle of the rudder to be `angle` degrees

#### def __sail__(self, angle):

Set the angle of the sail to `angle` degrees

