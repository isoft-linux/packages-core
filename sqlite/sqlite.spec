%global build_with_check 1 
%global snapshot_build 0 

%define realname sqlite-autoconf
%define realver 3090000
Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.9.0
Release: 3 
License: Public Domain
URL: http://www.sqlite.org/

%if %snapshot_build
#fossil clone http://www.sqlite.org/cgi/src sqlite.clone
#mkdir sqlite3
#cd sqlite3
#fossil open ../sqlite.clone
Source: sqlite3.tar.gz
%else
Source: http://www.sqlite.org/%{realname}-%{realver}.tar.gz
%endif

BuildRequires: ncurses-devel readline-devel

%if %snapshot_build
BuildRequires: tcl-devel
%endif

%if %build_with_check 
BuildRequires: tcl-devel
%endif


%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine.
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%if %snapshot_build
%setup -q -n sqlite3
%else
%setup -q -n %{realname}-%{realver}
%endif

%build
export LDFLAGS+="-lm"
export CFLAGS+="$CFLAGS -DSQLITE_ENABLE_FTS3=1 -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_SECURE_DELETE -DSQLITE_ENABLE_UNLOCK_NOTIFY -DSQLITE_ENABLE_RTREE=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 -DSQLITE_USE_URI -DSQLITE_ENABLE_FTS5=1 -DSQLITE_ENABLE_JSON1=1 -Iext/fts3"
%configure \
        --enable-threadsafe \
        --disable-static \
        --enable-readline \
        --enable-dynamic-extensions

%if %snapshot_build
make sqlite3.c
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1


%check
%if %build_with_check 
#root test will fail
make test ||: 
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man?/*

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 23 2015 cjacker - 3.9.0-3
- Rebuild for new 4.0 release

* Thu Oct 15 2015 Cjacker <cjacker@foxmail.com>
- update to 3.9.0
- enable SQLITE_ENABLE_JSON1 and SQLITE_ENABLE_FTS5
 
* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- rebuild with SQLITE_ENABLE_DBSTAT_VTAB, firefox >= 41.0 need it. 
