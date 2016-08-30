Summary: A tool for determining compilation options
Name: pkgconfig
Version: 0.29.1
Release: 1
License: GPL
URL: http://pkgconfig.freedesktop.org
Source0: http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz

BuildRequires: autoconf, automake, libtool

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

sed -i "s/CFLAGS = -g -O2/CFLAGS = -g -O2 -Wno-error=format-nonliteral/g" Makefile

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
rm -rf $RPM_BUILD_ROOT%{_docdir}

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
* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 0.29.1-1
- update pkg-config to 0.29.1

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 0.29-4
- Update

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 1:0.28-3
- Rebuild

* Fri Oct 23 2015 cjacker - 1:0.28-2
- Rebuild for new 4.0 release

