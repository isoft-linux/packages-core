Summary: A library for password generation and password quality checking
Name: libpwquality
Version: 1.2.4
Release: 7%{?dist}
# The package is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
License: BSD or GPLv2+
Source0: http://fedorahosted.org/releases/l/i/libpwquality/libpwquality-%{version}.tar.bz2
Patch0: libpwquality-support-disable-dict-check.patch
 
%global _pwqlibdir %{_libdir}
%global _moduledir %{_libdir}/security
%global _secconfdir %{_sysconfdir}/security

Requires: cracklib-dicts >= 2.8
Requires: pam%{?_isa}
BuildRequires: cracklib-devel
BuildRequires: gettext
BuildRequires: pam-devel
BuildRequires: python2-devel
BuildRequires: python3-devel

URL: http://libpwquality.fedorahosted.org/

# we don't want to provide private python extension libs
%define __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\.so$.

%description
This is a library for password quality checks and generation
of random passwords that pass the checks.
This library uses the cracklib and cracklib dictionaries
to perform some of the checks.

%package devel
Summary: Support for development of applications using the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files needed for development of applications using the libpwquality
library.
See the pwquality.h header file for the API.

%package -n python-pwquality
Summary: Python bindings for the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}

%description -n python-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%package -n python3-pwquality
Summary: Python bindings for the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}

%description -n python3-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%prep
%setup -q
%patch0 -p1

rm -rf %{py3dir}
cp -a . %{py3dir}

%build
%configure \
	--with-securedir=%{_moduledir} \
	--with-pythonsitedir=%{python_sitearch} \
	--with-python-binary=%{__python2} \
	--disable-static

make %{?_smp_mflags}

pushd %{py3dir}
%configure \
	--with-securedir=%{_moduledir} \
	--with-pythonsitedir=%{python3_sitearch} \
	--with-python-binary=%{__python3} \
	--disable-static

make %{?_smp_mflags}
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

pushd %{py3dir}
make -C python install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
popd

%if "%{_pwqlibdir}" != "%{_libdir}"
pushd $RPM_BUILD_ROOT%{_libdir}
mv libpwquality.so.* $RPM_BUILD_ROOT%{_pwqlibdir}
ln -sf %{_pwqlibdir}/libpwquality.so.*.* libpwquality.so
popd
%endif
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_moduledir}/*.la

%find_lang libpwquality

%check
# Nothing yet

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libpwquality.lang
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_moduledir}/pam_pwquality.so
%{_pwqlibdir}/libpwquality.so.*
%config(noreplace) %{_secconfdir}/pwquality.conf
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/pwquality.h
%{_libdir}/libpwquality.so
%{_libdir}/pkgconfig/*.pc

%files -n python-pwquality
%defattr(-,root,root,-)
%{python_sitearch}/pwquality.so
%{python_sitearch}/*.egg-info

%files -n python3-pwquality
%defattr(-,root,root,-)
%{python3_sitearch}/*.so
%{python3_sitearch}/*.egg-info

%changelog
* Wed Dec 23 2015 Cjacker <cjacker@foxmail.com> - 1.2.4-7
- Support nodictcheck

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 1.2.4-6
- Rebuild with python 3.5

* Fri Oct 23 2015 cjacker - 1.2.4-5
- Rebuild for new 4.0 release

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- first build.
