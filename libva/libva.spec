Name:		libva
Version:	1.6.1
Release:	2
Summary:	Video Acceleration (VA) API for Linux
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva/libva-%{version}.tar.bz2

BuildRequires:	libudev-devel
BuildRequires:	libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:	mesa-libGLES-devel
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-server) >= 1

%description
Libva is a library providing the VA API video acceleration API.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	utils
Summary:	Tools for %{name} (including vainfo)
Requires:	%{name}%{_isa} = %{version}-%{release}

%description	utils
The %{name}-utils package contains tools that are provided as part
of %{name}, including the vainfo tool for determining what (if any)
%{name} support is available on a system.

%prep
%setup -q

%build
%configure --disable-static \
  --enable-glx \
  --enable-x11 \
  --enable-egl \
  --enable-wayland

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libva*.so.*
# Keep these specific: if any new real drivers start showing up
# in libva, we need to know about it so they can be patent-audited
%{_libdir}/dri/dummy_drv_video.so

%files devel
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc

%files utils
%{_bindir}/vainfo
%{_bindir}/loadjpeg
%{_bindir}/avcenc
%{_bindir}/h264encode
%{_bindir}/mpeg2vldemo
%{_bindir}/mpeg2vaenc
%{_bindir}/jpegenc
%{_bindir}/putsurface
%{_bindir}/putsurface_wayland

%changelog
* Fri Oct 23 2015 cjacker - 1.6.1-2
- Rebuild for new 4.0 release

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.1


* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

