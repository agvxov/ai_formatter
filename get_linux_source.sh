#!/bin/sh

mkdir "training_set/linux"
find /usr/src/linux/ -type f -name "*.c" -exec cp --verbose {} "training_set/linux/" \;
