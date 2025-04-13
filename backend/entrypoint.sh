#!/bin/sh
chmod 666 /dev/ttyACM0
chmod 666 /dev/ttyACM1
exec "$@"
