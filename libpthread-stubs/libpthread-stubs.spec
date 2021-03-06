Summary: pthread-stubs provides weak aliases for pthread functions not provided in libc or otherwise available by default 
Name: libpthread-stubs 
Version: 0.3
Release: 3 
License: MIT
Source0: http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
pthread-stubs provides weak aliases for pthread functions not provided in libc or otherwise available by default

%package        devel
Summary:        Development files for %{name}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

pthread-stubs provides weak aliases for pthread functions 
not provided in libc or otherwise available by default

%prep
%setup -q -n %{name}-%{version}
%build
%configure 
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig
%changelog
* Fri Oct 23 2015 cjacker - 0.3-3
- Rebuild for new 4.0 release

