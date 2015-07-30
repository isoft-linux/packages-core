Summary: A library of handy utility functions
Name: glib2
Version: 2.45.3
Release: 2 
License: LGPL
Group: Core/Runtime/Library
URL: http://www.gtk.org
Source: glib-%{version}.tar.xz
Source2: glib2.sh
Source3: glib2.csh

BuildRequires: pkgconfig >= 0.8
BuildRequires: gettext
BuildRequires: libffi-devel
BuildRequires: python

%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.

This package provides version 2 of GLib.

%package devel
Summary: The GIMP ToolKit (GTK+) and GIMP Drawing Kit (GDK) support library
Group: Core/Development/Library
Requires: pkgconfig >= 1:0.8
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

%prep
%setup -q -n glib-%{version}

%build
%configure \
    --enable-static \
    --disable-fam \
    --enable-man
 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## glib2.sh and glib2.csh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d


#fix python path, it will affect the requirments of a rpm.
sed -i 's@#!/bin/python@#!/usr/bin/python@g' $RPM_BUILD_ROOT/%{_bindir}/gdbus-codegen
sed -i 's@#!/bin/python@#!/usr/bin/python@g' $RPM_BUILD_ROOT/%{_bindir}/gtester-report

%find_lang glib20

rpmclean

%check
#requires dbus-launch, since we seperate it to dbus-x11 package
#some gdbus test will failed.
make check ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f glib20.lang 
%defattr(-, root, root)
%{_bindir}/gapplication
%{_bindir}/gdbus
%{_bindir}/gio-querymodules
%{_bindir}/glib-compile-schemas
%{_bindir}/gresource
%{_bindir}/gsettings

%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%{_libdir}/gio/modules
%{_sysconfdir}/profile.d/*
%{_datadir}/bash-completion/completions/*
%dir %{_datadir}/glib-2.0/schemas
%{_datadir}/glib-2.0/schemas/*
%{_mandir}/man1/gapplication.1.gz
%{_mandir}/man1/gdbus.1.gz
%{_mandir}/man1/gio-querymodules.1.gz
%{_mandir}/man1/glib-compile-resources.1.gz
%{_mandir}/man1/glib-compile-schemas.1.gz
%{_mandir}/man1/gobject-query.1.gz
%{_mandir}/man1/gresource.1.gz
%{_mandir}/man1/gsettings.1.gz

%files devel
%defattr(-, root, root)
%{_bindir}/glib-compile-resources
%{_bindir}/gobject-query
%{_bindir}/gdbus-codegen 
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gtester
%{_bindir}/gtester-report
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%dir %{_datadir}/gtk-doc/
%{_datadir}/gtk-doc/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/glib-2.0/codegen
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/gdb/auto-load/usr/%{_lib}/*.py
%{_mandir}/man1/gtester-report.1.gz
%{_mandir}/man1/gtester.1.gz
%{_mandir}/man1/gdbus-codegen.1.gz
%{_mandir}/man1/glib-mkenums.1.gz
%{_mandir}/man1/glib-genmarshal.1.gz
%{_mandir}/man1/glib-gettextize.1.gz

%changelog
