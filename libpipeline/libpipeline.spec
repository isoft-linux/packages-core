%global gnulib_ver 20140202

Summary: A pipeline manipulation library
Name: libpipeline
Version: 1.4.1
Release: 4
License: GPLv3+
URL: http://libpipeline.nongnu.org/
Source: http://download.savannah.gnu.org/releases/libpipeline/libpipeline-%{version}.tar.gz

BuildRequires: libtool, check-devel

# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}

%description
libpipeline is a C library for setting up and running pipelines of
processes, without needing to involve shell command-line parsing which is
often error-prone and insecure. This alleviates programmers of the need to
laboriously construct pipelines using lower-level primitives such as fork(2)
and execve(2).

%package devel
Summary: Header files and libraries for pipeline manipulation library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
libpipeline-devel contains the header files and libraries needed
to develop programs that use libpipeline library.

%prep
%setup -q

%build
%{configure}
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'
rm $RPM_BUILD_ROOT/%{_libdir}/libpipeline.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README ChangeLog NEWS
%{_libdir}/libpipeline.so.*

%files devel
%{_libdir}/libpipeline.so
%{_libdir}/pkgconfig/libpipeline.pc
%{_includedir}/*.h
%{_mandir}/man3/*

%changelog
* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 1.4.1-4
- Remove Group from spec

* Wed Nov 04 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 1.4.1-3
- rebuilt

* Wed Nov 04 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 1.4.1-2
- init for isoft.
