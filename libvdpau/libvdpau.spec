Name:           libvdpau
Version:        1.1.1 
Release:        2 
Summary:        Wrapper library for the Video Decode and Presentation API

License:        MIT
URL:            http://freedesktop.org/wiki/Software/VDPAU
Source0:        http://cgit.freedesktop.org/~aplattner/libvdpau/snapshot/libvdpau-%{version}.tar.bz2

BuildRequires:  libtool

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  xorg-x11-proto-devel


%description
VDPAU is the Video Decode and Presentation API for UNIX. 
It provides an interface to video decode acceleration and presentation
hardware present in modern GPUs.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_trace.so*

%files devel
%{_includedir}/vdpau/
%{_libdir}/libvdpau.so
%{_libdir}/pkgconfig/vdpau.pc
%{_docdir}/libvdpau

%changelog
* Tue Sep 01 2015 Cjacker <cjacker@foxmail.com>
- Fix CVE-2015-5198, CVE-2015-5199, and CVE-2015-5200 for more details.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

