#!/bin/sh

/usr/lib/rpm/find-provides "$@" | grep -v 'perl('
exit 0
