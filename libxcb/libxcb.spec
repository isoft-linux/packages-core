Name:           libxcb
Version:        1.11
Release:        1.git 
Summary:        A C binding to the X11 protocol
License:        MIT
URL:            http://xcb.freedesktop.org/
#Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
#git clone git://anongit.freedesktop.org/git/xcb/libxcb
Source0:        libxcb.tar.gz

BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  libXau-devel
BuildRequires:  libxslt
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-util-macros
BuildRequires:  xcb-proto

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}

%description    doc
The %{name}-doc package contains documentation for the %{name} library.

%prep
%setup -q -n libxcb

%build
./autogen.sh
%configure \
    --disable-static \
    --enable-xkb \
    --enable-xinput \
    --docdir=%{_datadir}/doc/%{name}-%{version}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/xcb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_docdir}/%{name}-%{version}
%{_mandir}/man3/*

