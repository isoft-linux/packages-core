Name:           tslib
Version:        1.0
Release:        11%{?dist}
Summary:        Touchscreen Access Library

License:        LGPLv2
URL:            http://tslib.berlios.de/
Source0:        http://download.berlios.de/tslib/tslib-%{version}.tar.bz2
Patch0:         tslib-1.0-backport-O_CREAT.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool


%description
The idea of tslib is to have a core library that provides standardised
services, and a set of plugins to manage the conversion and filtering as
needed.

The plugins for a particular touchscreen are loaded automatically by the
library under the control of a static configuration file, ts.conf.
ts.conf gives the library basic configuration information.  Each line
specifies one module, and the parameters for that module.  The modules
are loaded in order, with the first one processing the touchscreen data
first. 


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p2 -b .ocreat
./autogen.sh

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%config(noreplace) %{_sysconfdir}/ts.conf
%{_bindir}/ts*
%{_libdir}/*.so.*
%dir %{_libdir}/ts
%{_libdir}/ts/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/tslib.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/tslib-0.0.pc


%changelog
* Fri Oct 23 2015 cjacker - 1.0-11
- Rebuild for new 4.0 release

