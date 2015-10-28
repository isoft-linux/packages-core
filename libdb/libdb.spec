%define __soversion_major 6 
%define __soversion %{__soversion_major}.1

Summary: The Berkeley DB database library for C
Name: libdb
Version: 6.1.23
Release: 2 
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
URL:    http://www.oracle.com/technetwork/database/database-technologies/berkeleydb/overview/index.html
License: BSD
BuildRequires: perl
Conflicts: filesystem < 3

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB databases
Requires: %{name} = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB library
Requires: %{name} = %{version}-%{release}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-doc
Summary: C development documentation files for the Berkeley DB library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description devel-doc
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package static
Summary: Berkeley DB static libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require static linking of
Berkeley DB.

%package cxx-devel
Summary: The Berkeley DB database library for C++
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description cxx-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package sql-devel
Summary: Development files for using the Berkeley DB with sql
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description sql-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%prep
%setup -q -n db-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"; export CFLAGS

build() {
	test -d dist/$1 || mkdir dist/$1
	pushd dist/$1
	ln -sf ../configure .
	# XXX --enable-diagnostic should be disabled for production (but is
	# useful).
	# XXX --enable-debug_{r,w}op should be disabled for production.
	%configure -C \
		--enable-shared \
        --enable-static \
		--enable-cxx \
        --enable-sql \
        --enable-dbm \
		--disable-rpath 

	make %{?_smp_mflags}
	popd
}

build dist-tls

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a,libdb_sql.a}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx-%{__soversion_major}.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_sql-%{__soversion_major}.so

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
for i in db.h db_cxx.h; do
	ln -s %{name}/$i ${RPM_BUILD_ROOT}%{_includedir}
done

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# avoid fancy permissons
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/*.so

# unify documentation and examples, remove stuff we don't need
rm -rf docs/csharp
rm -rf examples/csharp
rm -rf docs/installation
mv examples docs


%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post cxx-devel -p /sbin/ldconfig

%postun cxx-devel -p /sbin/ldconfig

%post sql-devel -p /sbin/ldconfig

%postun sql-devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libdb-%{__soversion}.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdb.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db.h
%{_includedir}/db_cxx.h

%files devel-doc
%defattr(-,root,root,-)
%doc	docs/*

%files static
%defattr(-,root,root,-)
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_sql-%{__soversion}.a

%files cxx-devel
%defattr(-,root,root,-)
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-%{__soversion}.so

%files sql-devel
%defattr(-,root,root,-)
%{_bindir}/dbsql
%{_libdir}/libdb_sql.so
%{_libdir}/libdb_sql-%{__soversion}.so
%{_includedir}/%{name}/dbsql.h

%changelog
* Fri Oct 23 2015 cjacker - 6.1.23-2
- Rebuild for new 4.0 release

