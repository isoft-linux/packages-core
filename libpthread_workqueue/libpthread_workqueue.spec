Name:       libpthread_workqueue 
Summary:    thread pool library
Version:    0.9.2
Release:    2
License:    BSD
Url:        https://github.com/mheily/libpwq/releases

Source0:    libpwq-%version.tar.gz
Patch0:	libpwq-fix-Werror.patch

%description
The pthread_workqueue library allows you to create one or more workqueues and submit work items for processing. The workqueues are serviced by a thread pool that is automatically created and dynamically managed by the library.

The API is based on the pthread_workqueue API in FreeBSD 8.0, which was designed to be compatible with the API developed by Apple Inc to support the Grand Central Dispatch concurrency framework.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n libpwq-%{version} 
%patch0 -p1

%build
export CC=clang
autoreconf -ivf
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

%check
make check

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_mandir}/man3/*
%changelog
* Fri Oct 23 2015 cjacker - 0.9.2-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

