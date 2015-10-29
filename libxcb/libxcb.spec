%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       libxcb
Version:    1.11.1
Release:    9.git%{?dist}
Summary:    A C binding to the X11 protocol
License:    MIT
URL:        http://xcb.freedesktop.org/

#Source0:    http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
Source0: libxcb.tar.gz
#Patch0: libxcb-not-close-fd.patch
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(xau) >= 0.99.2
BuildRequires:  pkgconfig(xcb-proto) >= 1.11
BuildRequires:  pkgconfig(xorg-macros) >= 1.18
BuildRequires:  pkgconfig(xdmcp) 
BuildRequires: libpthread-stubs-devel

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%autosetup -n %{name} -p1

%build
if [ ! -f configure ]; then ./autogen.sh; fi
%configure \
    --disable-static \
    --disable-selinux \
    --enable-xkb \
    --enable-xinput \
    --enable-xevie \
    --disable-xprint \
    --disable-silent-rules \
    --with-queue-size=65536

# Remove rpath from libtool (extra insurance if autoreconf is ever dropped)
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libxcb-composite.so.0*
%{_libdir}/libxcb-damage.so.0*
%{_libdir}/libxcb-dpms.so.0*
%{_libdir}/libxcb-dri2.so.0*
%{_libdir}/libxcb-dri3.so.0*
%{_libdir}/libxcb-glx.so.0*
%{_libdir}/libxcb-present.so.0*
%{_libdir}/libxcb-randr.so.0*
%{_libdir}/libxcb-record.so.0*
%{_libdir}/libxcb-render.so.0*
%{_libdir}/libxcb-res.so.0*
%{_libdir}/libxcb-screensaver.so.0*
%{_libdir}/libxcb-shape.so.0*
%{_libdir}/libxcb-shm.so.0*
%{_libdir}/libxcb-sync.so.1*
%{_libdir}/libxcb-xevie.so.0*
%{_libdir}/libxcb-xf86dri.so.0*
%{_libdir}/libxcb-xfixes.so.0*
%{_libdir}/libxcb-xinerama.so.0*
%{_libdir}/libxcb-xinput.so.0*
%{_libdir}/libxcb-xkb.so.1*
#%{_libdir}/libxcb-xselinux.so.0*
%{_libdir}/libxcb-xtest.so.0*
%{_libdir}/libxcb-xv.so.0*
%{_libdir}/libxcb-xvmc.so.0*
%{_libdir}/libxcb.so.1*

%files devel
%{_includedir}/xcb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_docdir}/libxcb
%{_mandir}/man3/*.3*


%changelog
* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 1.11.1-9.git
- Rebuild with new xcb-proto

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 1.11.1-8.git
- Rebuild

* Fri Oct 23 2015 cjacker - 1.11.1-7.git
- Rebuild for new 4.0 release

* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com>
- libxcb git 

