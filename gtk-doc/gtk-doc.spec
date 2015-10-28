Summary: API documentation generation tool for GTK+ and GNOME
Name: gtk-doc
Version: 1.24
Release: 6
License: GPLv2+ and GFDL
Source: http://ftp.gnome.org/pub/GNOME/sources/gtk-doc/1.19/gtk-doc-%{version}.tar.xz
BuildArch: noarch
URL: http://www.gtk.org/gtk-doc

BuildRequires: docbook-utils 
BuildRequires: jade 
BuildRequires: libxslt 
BuildRequires: docbook-style-xsl
BuildRequires: python
BuildRequires: itstool
Requires: docbook-utils jade /usr/bin/cmp libxslt docbook-style-xsl
# we are installing an automake macro
Requires: automake
# we are installing a .pc file
Requires: pkgconfig
# we are installing a .omf file
Requires: sgml-common

Source1: filter-requires-gtk-doc.sh
%define __perl_requires %{SOURCE1}

%description
gtk-doc is a tool for generating API reference documentation.
It is used for generating the documentation for GTK+, GLib
and GNOME.

%prep

%setup -q

mv doc/README doc/README.docs

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

sed -i 's@#!/bin/python@#!/usr/bin/env python@g' $RPM_BUILD_ROOT%{_bindir}/gtkdoc-depscan 
rm -rf $RPM_BUILD_ROOT/var/scrollkeeper

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html

%clean
rm -rf $RPM_BUILD_ROOT

%post 

%postun

%files
%defattr(-, root, root)
%doc AUTHORS README doc/* examples COPYING COPYING-DOCS
%{_bindir}/*
%{_datadir}/aclocal/gtk-doc.m4
%{_datadir}/gtk-doc/
%{_datadir}/sgml/gtk-doc/
%{_datadir}/pkgconfig/gtk-doc.pc
%{_datadir}/help/*/gtk-doc-manual

%changelog
* Fri Oct 23 2015 cjacker - 1.24-6
- Rebuild for new 4.0 release

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

