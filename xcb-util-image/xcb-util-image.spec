Name:		xcb-util-image
Version:	0.4.0
Release: 2 
Summary:	Port of Xlib's XImage and XShmImage functions on top of libxcb
Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-image module provides the following library:

  - image: Port of Xlib's XImage and XShmImage functions.


%package 	devel
Summary:	Development and header files for xcb-util-image
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-image.


%prep
%setup -q


%build
%configure --with-pic --disable-static --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm %{buildroot}%{_libdir}/*.la

%check
make check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*


%files devel
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h


%changelog
