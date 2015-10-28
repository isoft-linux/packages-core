
Name:           libxkbcommon
Version:        0.5.0
Release:        3
Summary:        X.Org X11 XKB parsing library
License:        MIT
URL:            http://www.x.org

Source0:        http://xkbcommon.org/download/%{name}-%{version}.tar.xz

BuildRequires:  autoconf automake libtool
BuildRequires:  xorg-x11-util-macros byacc flex bison
BuildRequires:  xorg-x11-proto-devel libX11-devel
BuildRequires:  xkeyboard-config-devel
%global x11 1
BuildRequires:  pkgconfig(xcb-xkb) >= 1.10

Requires:       xkeyboard-config

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package devel
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
X.Org X11 XKB parsing development package

%package x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%package x11-devel
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}

%description x11-devel
X.Org X11 XKB keymap creation library development package

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

autoreconf -v --install || exit 1

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  %{?x11:--enable-x11}%{!?x11:--disable-x11}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0

%files devel
%{_libdir}/libxkbcommon.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_libdir}/pkgconfig/xkbcommon.pc
%{_docdir}/libxkbcommon

%if 0%{?x11}
%post x11 -p /sbin/ldconfig
%postun x11 -p /sbin/ldconfig

%files x11
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-devel
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc
%endif

%changelog
* Fri Oct 23 2015 cjacker - 0.5.0-3
- Rebuild for new 4.0 release

