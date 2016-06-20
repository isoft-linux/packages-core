Summary: A library of handy utility functions
Name: glib2
Version: 2.48.0
Release: 2
License: LGPL
URL: http://www.gtk.org
%global versiondir %(echo %{version} | cut -d. -f1-2)

Source: http://ftp.gnome.org/pub/GNOME/sources/glib/%{versiondir}/glib-%{version}.tar.xz

Source2: glib2.sh
Source3: glib2.csh

BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: libffi-devel
BuildRequires: python
BuildRequires: libattr-devel
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: zlib-devel
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python-devel
BuildRequires: libelfutils-devel
BuildRequires: chrpath
BuildRequires: pcre-devel

# required for GIO content-type support
Requires: shared-mime-info

%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.

This package provides version 2 of GLib.

%package devel
Summary: The GIMP ToolKit (GTK+) and GIMP Drawing Kit (GDK) support library
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

%prep
%setup -q -n glib-%{version}

%build
%configure \
    --disable-systemtap \
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
* Tue Apr 19 2016 sulit <sulitsrc@gmail.com> - 2.48.0-2
- update to release 2.48.0
- add buildrequire pcre-devel

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.46.2-2
- Update to match gnome-3.18.2

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 2.46.1-4
- Rebuild, fix pkgconfig requires, fix build requires

* Fri Oct 23 2015 cjacker - 2.46.1-3
- Rebuild for new 4.0 release

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 2.46.1

* Thu Sep 24 2015 Cjacker <cjacker@foxmail.com>
- update to 2.46.0 with gnome 3.18

* Wed Sep 16 2015 Cjacker <cjacker@foxmail.com>
- update to 2.45.8

* Fri Aug 21 2015 Cjacker <cjacker@foxmail.com>
- update to 2.45.6
- fix inotify issue.
