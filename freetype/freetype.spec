%define _localedir %{_datadir}/locale

Summary: A free and portable TrueType font rendering engine.
Name: freetype
Version: 2.6
Release: 7 
License: GPL
URL: http://www.freetype.org
Source0:  freetype-%{version}.tar.bz2
Source1:  infinality-settings.sh

#there two patch is very important to improve font rendering result.
#be careful when update !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#By Cjacker
Patch0:  freetype-2.5.3-enable-valid.patch  
Patch1:  03-infinality-2.6-2015.06.08.patch

Patch10:  freetype-disable-make-detect.patch
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
%patch10 -p1

%build
# Build Freetype 2
export CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"
%configure --without-png --without-harfbuzz 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


rm -fr $RPM_BUILD_ROOT%{_localedir}
cp -r include/internal $RPM_BUILD_ROOT/usr/include/freetype2/

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
%{_libdir}/libfreetype.a
%{_libdir}/pkgconfig/freetype2.pc
%{_bindir}/freetype-config


%changelog
* Fri Oct 23 2015 cjacker - 2.6-7
- Rebuild for new 4.0 release

