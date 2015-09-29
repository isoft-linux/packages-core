%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           gobject-introspection
Version:        1.46.0
Release:        1
Summary:        Introspection system for GObject-based libraries

Group:  Core/Runtime/Library 
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection

Source0:        ftp://ftp.gnome.org/pub/gnome/sources/gobject-introspection/1.44/gobject-introspection-%{version}.tar.xz
BuildRequires:  glib2-devel
BuildRequires:  python-devel >= 2.5
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libffi-devel
BuildRequires:  chrpath
BuildRequires:  libxml2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package devel
Summary: Libraries and headers for gobject-introspection
Group:  Core/Development/Library
Requires: %name = %{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description devel
Libraries and headers for gobject-introspection

%prep
%setup -q

%build
%configure --disable-gtk-doc
make V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

sed -i 's@#!/bin/python@#!/usr/bin/env python@g' $RPM_BUILD_ROOT/%{_bindir}/g-ir-annotation-tool
sed -i 's@#!/bin/python@#!/usr/bin/env python@g' $RPM_BUILD_ROOT/%{_bindir}/g-ir-scanner


# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/g-ir-{compiler,generate}
# Mistake in upstream automake
rm -f $RPM_BUILD_ROOT/%{_bindir}/barapp

# Move the python modules to the correct location
mkdir -p $RPM_BUILD_ROOT/%{python_sitearch}
mv $RPM_BUILD_ROOT/%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT/%{python_sitearch}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING

%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/gobject-introspection-1.0
%{_datadir}/aclocal/introspection.m4
%{python_sitearch}/giscanner
%{_mandir}/man1/*.gz

%changelog
* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to gnome 3.18
