Name:      icu
Version:   56.2
Release:   1
Summary:   International Components for Unicode
License:   MIT and UCD and Public Domain
URL:       http://www.icu-project.org/

%global version_major %(echo %{version} | cut -d. -f1)
%global version_minor %(echo %{version} | cut -d. -f2)

Source0:   http://download.icu-project.org/files/icu4c/%{version}/icu4c-%{version_major}_%{version_minor}-src.tgz
Patch1: icu.8198.revert.icu5431.patch
Patch2: icu.8800.freeserif.crash.patch
Patch3: icu.7601.Indic-ccmp.patch

BuildRequires: doxygen, autoconf, python
Requires: lib%{name} = %{version}-%{release}

%description
Tools and utilities for developing with icu.

%package -n lib%{name}
Summary: International Components for Unicode - libraries

%description -n lib%{name}
The International Components for Unicode (ICU) libraries provide
robust and full-featured Unicode services on a wide variety of
platforms. ICU supports the most current version of the Unicode
standard, and they provide support for supplementary Unicode
characters (needed for GB 18030 repertoire support).
As computing environments become more heterogeneous, software
portability becomes more important. ICU lets you produce the same
results across all the various platforms you support, without
sacrificing performance. It offers great flexibility to extend and
customize the supplied services.

%package  -n lib%{name}-devel
Summary:  Development files for International Components for Unicode
Requires: lib%{name} = %{version}-%{release}
Requires: pkgconfig

%description -n lib%{name}-devel
Includes and definitions for developing with icu.

%package -n lib%{name}-doc
Summary: Documentation for International Components for Unicode

%description -n lib%{name}-doc
%{summary}.

%prep
%setup -q -n %{name}
%patch1 -p2 -R -b .icu8198.revert.icu5431.patch
%patch2 -p1 -b .icu8800.freeserif.crash.patch
%patch3 -p1 -b .icu7601.Indic-ccmp.patch

%build
#if clang found, icu will use clang by default.

export CC=cc
export CXX=c++

cd source
%configure --with-data-packaging=library --disable-samples
make %{?_smp_mflags} 
#make doc

%install
rm -rf $RPM_BUILD_ROOT source/__docs
make -C source install DESTDIR=$RPM_BUILD_ROOT
#make -C source install-doc docdir=__docs

%check
#without LANG/LC_ALL settings, a little test may failed.
LANG=C LC_ALL=C make check -C source

%clean
rm -rf $RPM_BUILD_ROOT

%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/genrb
%{_bindir}/gendict
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%{_sbindir}/*
%{_mandir}/man1/derb.1*
%{_mandir}/man1/gencnval.1*
%{_mandir}/man1/genrb.1*
%{_mandir}/man1/genbrk.1*
%{_mandir}/man1/gencfu.1*
%{_mandir}/man1/gendict.1*
%{_mandir}/man1/makeconv.1*
%{_mandir}/man1/pkgdata.1*
%{_mandir}/man1/uconv.1*
%{_mandir}/man8/*.8*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc license.html readme.html
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/icuinfo
%{_mandir}/man1/%{name}-config.1*
%{_includedir}/layout
%{_includedir}/unicode
%{_libdir}/*.so
%{_libdir}/pkgconfig/icu*.pc
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%{_datadir}/%{name}/%{version}/install-sh
%{_datadir}/%{name}/%{version}/mkinstalldirs
%{_datadir}/%{name}/%{version}/config
%doc %{_datadir}/%{name}/%{version}/license.html

#%files -n lib%{name}-doc
#%defattr(-,root,root,-)
#%doc license.html readme.html
#%doc source/__docs/%{name}/html/*

%changelog
* Thu Dec 15 2016 sulit - 56.2-1
- update icu to 58.2

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 56.1-6
- Update

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 56.1-5
- Update to 56.1

* Sat Oct 24 2015 cjacker - 55.1-4
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

