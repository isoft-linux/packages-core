Name:           libGLU
Version:        9.0.0
Release:        2 
Summary:        Mesa libGLU runtime library
License:        MIT
Source0:        glu-%{version}.tar.bz2
Patch1: 0001-glu-initialize-PriorityQ-order-field-to-NULL-in-pqNe.patch
Patch2: 0002-Add-D-N-DEBUG-to-CFLAGS-dependent-on-enable-debug.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  mesa-libGL-devel
Provides:   mesa-libGLU

%description
Mesa libGLU runtime library

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
provides:       mesa-libGLU-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n glu-%{version}
%patch1 -p1
%patch2 -p1

%build
%configure \
    --disable-static
 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/GL/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 23 2015 cjacker - 9.0.0-2
- Rebuild for new 4.0 release

* Fri Jul 10 2015 cjacker <cjacker@foxmail.com>
- rebuild with mesa 10.7.0 git.
