Summary:        Library for accessing USB devices
Name:           libusb
Version:        1.0.19
Release:        2
Source0:        http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
License:        LGPLv2+
URL:            http://sourceforge.net/apps/mediawiki/libusb/
Provides:       libusb1 = %{version}-%{release}
Provides:       libusbx = %{version}-%{release}

%description
This package provides a way for applications to access USB devices.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libusb1-devel = %{version}-%{release}
Provides:       libusbx-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static --enable-examples-build
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%check
#no check at all
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/libusb-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/libusb-1.0.pc



%changelog
* Fri Oct 23 2015 cjacker - 1.0.19-2
- Rebuild for new 4.0 release

* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS

