#!/bin/sh

[[ $# < 1 ]] && exit 1

find "$1" -type f -name "*.c" \
    -exec vim +"set tabstop=8" +"set expandtab" +"retab" +wq {} \; \
    -exec sh -c 'converter.out accumulate "$1" > "$1.acc"' _ {} \; \
    -exec sh -c 'converter.out normalize "$1" > "$1.norm"' _ {} \;
