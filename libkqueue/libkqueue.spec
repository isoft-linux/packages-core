Name:       libkqueue
Summary:    Emulates the kqueue and kevent system calls
Version:    2.0.3
Release:    2
License:    BSD
Url:        https://github.com/mheily/libkqueue
#git clone https://github.com/mheily/libkqueue.git
Source0:    %{name}.tar.gz

%description
Emulates the kqueue and kevent system calls

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q  -n %{name}

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

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libkqueue.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/kqueue/sys/event.h
%{_libdir}/libkqueue.so
%{_libdir}/libkqueue.a
%{_libdir}/pkgconfig/libkqueue.pc
%{_mandir}/man2/*

%changelog
* Fri Oct 23 2015 cjacker - 2.0.3-2
- Rebuild for new 4.0 release

* Sat Jul 11 2015 Cjacker <cjacker@foxmail.com>
- update to git, pass "make check"
