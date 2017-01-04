%define _localedir %{_datadir}/locale

Summary: A free and portable TrueType font rendering engine.
Name: freetype
Version: 2.7
Release: 5
License: GPL
URL: http://www.freetype.org
Source0:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1:  freetype2.sh

Patch0:  0001-Enable-table-validation-modules.patch
Patch1:  0002-infinality-2.7-2016.09.09.patch
#Patch10: freetype-2.5.3-freetype-config-prefix.patch

BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

%description
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

%package devel
Summary: FreeType development libraries and header files
Requires: %{name} = %{version}-%{release}

%description devel
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%prep
%setup -q 
%patch0 -p1
%patch1 -p1

#%patch10 -p1

%build
# Build Freetype 2
export CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"
%configure --disable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

rm -fr $RPM_BUILD_ROOT%{_localedir}
cp -r include/freetype/internal $RPM_BUILD_ROOT%{_includedir}/freetype2/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/*.sh
%{_libdir}/libfreetype.so*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_datadir}/aclocal/freetype2.m4
%{_libdir}/pkgconfig/freetype2.pc
%{_bindir}/freetype-config
%{_mandir}/man1/freetype-config.1*

%changelog
* Wed Jan 04 2017 sulit - 2.7-5
- upgrade freetype to 2.7

* Thu Nov 24 2016 sulit <sulitsrc@163.com> - 2.7-3
- rebuild

* Tue Nov 22 2016 cjacker - 2.7-2
- Update to 2.7, update infinality patches

* Fri Nov 18 2016 cjacker - 2.7-2
- Update to 2.7

* Tue Dec 01 2015 Cjacker <cjacker@foxmail.com> - 2.6.2-2
- Update

* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 2.6.1-8
- Update

* Fri Oct 23 2015 cjacker - 2.6-7
- Rebuild for new 4.0 release

