Name:           libverto
Version:        0.2.6
Release:        6%{?dist}
Summary:        Main loop abstraction library

License:        MIT
URL:            https://fedorahosted.org/libverto/
Source0:        http://fedorahosted.org/releases/l/i/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  libevent-devel
%if !0%{?rhel}
BuildRequires:  libev-devel
%endif

%description
libverto provides a way for libraries to expose asynchronous interfaces
without having to choose a particular event loop, offloading this
decision to the end application which consumes the library.

If you are packaging an application, not library, based on libverto,
you should depend either on a specific implementation module or you
can depend on the virtual provides 'libverto-module-base'. This will
ensure that you have at least one module installed that provides io,
timeout and signal functionality. Currently glib is the only module
that does not provide these three because it lacks signal. However,
glib will support signal in the future.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        glib
Summary:        glib module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    glib
Module for %{name} which provides integration with glib.

This package does NOT yet provide %{name}-module-base.

%package        glib-devel
Summary:        Development files for %{name}-glib
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    glib-devel
The %{name}-glib-devel package contains libraries and header files for
developing applications that use %{name}-glib.

%package        libevent
Summary:        libevent module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libevent
Module for %{name} which provides integration with libevent.

%package        libevent-devel
Summary:        Development files for %{name}-libevent
Requires:       %{name}-libevent%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libevent-devel
The %{name}-libevent-devel package contains libraries and header files for
developing applications that use %{name}-libevent.

%package        libev
Summary:        libev module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libev
Module for %{name} which provides integration with libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%package        libev-devel
Summary:        Development files for %{name}-libev
Requires:       %{name}-libev%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libev-devel
The %{name}-libev-devel package contains libraries and header files for
developing applications that use %{name}-libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n %{name}-glib -p /sbin/ldconfig
%postun -n %{name}-glib -p /sbin/ldconfig

%post -n %{name}-libevent -p /sbin/ldconfig
%postun -n %{name}-libevent -p /sbin/ldconfig

%post -n %{name}-libev -p /sbin/ldconfig
%postun -n %{name}-libev -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/verto.h
%{_includedir}/verto-module.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files glib
%{_libdir}/%{name}-glib.so.*

%files glib-devel
%{_includedir}/verto-glib.h
%{_libdir}/%{name}-glib.so
%{_libdir}/pkgconfig/%{name}-glib.pc

%files libevent
%{_libdir}/%{name}-libevent.so.*

%files libevent-devel
%{_includedir}/verto-libevent.h
%{_libdir}/%{name}-libevent.so
%{_libdir}/pkgconfig/%{name}-libevent.pc

%files libev
%{_libdir}/%{name}-libev.so.*

%files libev-devel
%{_includedir}/verto-libev.h
%{_libdir}/%{name}-libev.so
%{_libdir}/pkgconfig/%{name}-libev.pc

%changelog
* Sat Oct 24 2015 cjacker - 0.2.6-6
- Rebuild for new 4.0 release

