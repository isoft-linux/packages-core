Name:		xcb-util
Version:	0.4.0
Release: 3	
Summary:	Convenience libraries sitting on top of libxcb

License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2

BuildRequires:	gperf, pkgconfig, libxcb-devel >= 1.4, m4, xorg-x11-proto-devel
BuildRequires:	chrpath


%description
The xcb-util module provides a number of libraries which sit on top of
libxcb, the core X protocol library, and some of the extension
libraries. These experimental libraries provide convenience functions
and interfaces which make the raw X protocol more usable. Some of the
libraries also provide client-side code which is not strictly part of
the X protocol but which have traditionally been provided by Xlib.


%package 	devel
Summary:	Development and header files for xcb-util
Requires:	%{name} = %{version}-%{release}, pkgconfig
%description	devel
Development files for xcb-util.


%prep
%setup -q 

%build
%configure --with-pic --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove RPATH
chrpath --delete $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libxcb-*.so.*


%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/libxcb*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
* Fri Oct 23 2015 cjacker - 0.4.0-3
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

