Summary: A tool for determining compilation options
Name: pkgconfig
Version: 0.28
Release: 1
Epoch: 1
License: GPL
URL: http://pkgconfig.freedesktop.org
Group:   Core/Development/Utility
Source:  http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%setup -n pkg-config-%{version} -q

%build
%configure \
    --with-internal-glib \
    --disable-shared \
    --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig 

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_docdir}
rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_bindir}/*
%dir %{_libdir}/pkgconfig
%dir %{_datadir}/pkgconfig
%{_datadir}/aclocal/*

%changelog
