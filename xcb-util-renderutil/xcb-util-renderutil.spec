Name:		xcb-util-renderutil
Version:	0.3.9
Release: 5
Summary:	Convenience functions for the Render extension
Group:		System Environment/Libraries
License:	MIT
URL:		http://xcb.freedesktop.org
Source0:	http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-renderutil module provides the following library:

  - renderutil: Convenience functions for the Render extension.


%package 	devel
Summary:	Development and header files for xcb-util-renderutil
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-renderutil.


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
