Summary: A GNU set of database routines which use extensible hashing
Name: gdbm
Version: 1.12
Release: 1
Source: http://ftp.gnu.org/gnu/gdbm/gdbm-%{version}.tar.gz
Patch0: gdbm-1.10-zeroheaders.patch

License: GPLv2+
URL: http://www.gnu.org/software/gdbm/
BuildRequires: libtool

%description
Gdbm is a GNU database indexing library, including routines which use
extensible hashing.  Gdbm works in a similar way to standard UNIX dbm
routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple
database routines, you should install gdbm.  You'll also need to
install gdbm-devel.

%package devel
Summary: Development libraries and header files for the gdbm library
Requires: %{name} = %{version}-%{release}

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep
%setup -q
%patch0 -p1 -b .zeroheaders

libtoolize --force --copy
aclocal
automake --add-missing 
autoconf

%build
%configure --disable-static --enable-libgdbm-compat

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

rm -rf $RPM_BUILD_ROOT%{_infodir}

%find_lang gdbm

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gdbm.lang
%defattr(-,root,root,-)
%{_bindir}/gdbm*

%{_libdir}/libgdbm.so.4*
%{_libdir}/libgdbm_compat.so.4*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm_compat.so
%{_includedir}/gdbm*
%{_includedir}/dbm.h
%{_includedir}/ndbm.h
%{_mandir}/man3/*
%{_mandir}/man1/*

%changelog
* Thu Dec 15 2016 sulit - 1.12-1
- upgrade gdbm to 1.12

* Fri Oct 23 2015 cjacker - 1.11-10
- Rebuild for new 4.0 release

