Summary: A system independent dlopen wrapper for GNU libtool 
Name:    libltdl
Version: 2.4.6
Release: 16
License: GPLv2+ and LGPLv2+ and GFDL
Group:   Core/Runtime/Library
Source:  http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz

URL:     http://www.gnu.org/software/libtool/

Provides: libtool-ltdl = %{version}-%{release} 

BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: gcc

%description
A system independent dlopen wrapper for GNU libtool.

%package devel
Summary: Tools needed for development using the GNU Libtool Dynamic Module Loader
Group:   Core/Development/Library

Provides: libtool-ltdl-devel = %{version}-%{release} 
Requires: %{name} = %{version}-%{release}
License:  LGPLv2+

%description devel
Libraries and header files for development with ltdl.

%prep
%setup -n libtool-%{version} -q

%build

export CFLAGS="$RPM_OPT_FLAGS -fPIC"

./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --mandir=%{_mandir} --infodir=%{_infodir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_libdir}/libltdl.la  %{buildroot}%{_libdir}/libltdl.a

#this files should be in libtool package.
rm -rf $RPM_BUILD_ROOT%{_bindir}/libtool
rm -rf $RPM_BUILD_ROOT%{_bindir}/libtoolize
rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal/*.m4
rm -rf $RPM_BUILD_ROOT%{_datadir}/libtool/config
rm -rf $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libltdl.so.*

%files devel
%defattr(-,root,root)
%{_datadir}/libtool/libltdl
%{_libdir}/libltdl.so
%{_includedir}/ltdl.h
%{_includedir}/libltdl

%changelog
