Summary: An XML parser library
Name: expat
Version: 2.2.0
Release: 1
Source: http://downloads.sourceforge.net/expat/expat-%{version}.tar.bz2
URL: http://www.libexpat.org/
License: MIT
BuildRequires: autoconf, automake, libtool

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and header files to develop applications using expat
Requires: expat = %{version}-%{release}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

%package static
Summary: expat XML parser static library
Requires: expat-devel%{?_isa} = %{version}-%{release}

%description static
The expat-static package contains the static version of the expat library.
Install it if you need to link statically with expat.

%prep
%setup -q

%build
#rm -rf autom4te*.cache
#libtoolize --copy --force --automake && aclocal && autoheader && autoconf
autoreconf -ivf
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT


%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a


%changelog
* Thu Dec 08 2016 sulit - 2.2.0-1
- upgrade expat to 2.2.0

* Fri Oct 23 2015 cjacker - 2.1.0-6
- Rebuild for new 4.0 release

