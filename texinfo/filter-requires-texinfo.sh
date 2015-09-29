#!/bin/sh

/usr/lib/rpm/find-provides "$@" | grep 'perl(\(Text::Unidecode\|Unicode::EastAsianWidth\|Data::Dumper\|Locale::Messages\))'
exit 0
