%define freetype2 freetype

Summary: Font configuration and customization library
Name: fontconfig
Version: 2.12.1
Release: 2
License: MIT
URL: http://fontconfig.org
Source0: http://fontconfig.org/release/fontconfig-%{version}.tar.bz2

Source1: fontconfig-ultimate-git.tar.bz2 

Source10: 99-lcd.conf

#NOTE, this config file will force monospace/serif automatch a English font.
#since there is no really monospace chinesefont we used.
Source11:   99-force-monospace-serif.conf
#disable bitmap of some fonts.
Source12:   25-no-bitmap.conf

BuildRequires: %{freetype2}-devel
BuildRequires: expat-devel
BuildRequires: perl
BuildRequires: automake
BuildRequires: libtool
Requires:coreutils
Requires(pre): %{freetype2}

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package devel
Summary:	Font configuration and customization library
Requires:	%{name} = %{version}-%{release}
Requires:	%{freetype2}-devel >= 2.1.4

%description devel
The fontconfig-devel package includes the static libraries, 
header files, and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%prep
%setup -q -a1
for i in fontconfig-ultimate-git/fontconfig_patches/0*.patch
do
    cat $i|patch -p1
done

cp -r  fontconfig-ultimate-git/conf.d.infinality .
aclocal
libtoolize -f
automake -afi

%build
FLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$FLAGS"
export CFLAGS="$FLAGS"
#   --with-templatedir=%{_sysconfdir}/fonts/conf.avail \
#   --with-xmldir=%{_sysconfdir}/fonts \
%configure \
   --with-add-fonts=/usr/X11R6/lib/X11/fonts \
   --with-default-fonts=%{_datadir}/fonts \
   --with-baseconfigdir=%{_sysconfdir}/fonts \
   --with-templateinfdir=%{_sysconfdir}/fonts/conf.avail.infinality \
   --disable-docs
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" 

cp -r fontconfig-ultimate-git/fontconfig_patches/{combi,free,ms} \
    %{buildroot}%{_sysconfdir}/fonts/conf.avail.infinality

install -m755 fontconfig-ultimate-git/fontconfig_patches/fc-presets %{buildroot}%{_bindir}/fc-presets

install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{_datadir}/fontconfig/conf.avail
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/fontconfig/conf.avail
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT/%{_datadir}/fontconfig/conf.avail

pushd $RPM_BUILD_ROOT/etc/fonts/conf.d
ln -sf %{_datadir}/fontconfig/conf.avail/99-lcd.conf ./99-lcd.conf
#this will cause some problems with old libXft based gui toolkit, such as fltk/fox fontrendering.
#But it's very useful for GTK/Qt display correctly.
#Display correctly not only means display Chinese/English characters, but also the font width, height and so on.
#for example, without this, input 'g' in gtk lineedit, you will find the bottom was cutted.
#this config means: always use Latin font display Latin character and let other languages auto-match.
#try fc-match Sans/fc-match Sans:lang=zh
#By Cjacker
ln -sf %{_datadir}/fontconfig/conf.avail/99-force-monospace-serif.conf ./99-force-monospace-serif.conf
ln -sf %{_datadir}/fontconfig/conf.avail/25-no-bitmap.conf ./25-no-bitmap.conf
popd



%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
{
  /sbin/ldconfig
  # Force regeneration of all fontconfig cache files.
  %{_bindir}/fc-cache -f 2>/dev/null
}
mkdir -p /usr/lib/X11/fonts/TrueType

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%config %{_sysconfdir}/fonts/fonts.conf
#%{_sysconfdir}/profile.d/*.sh
%{_sysconfdir}/fonts
%{_bindir}/fc-*
%{_libdir}/*.so.*
#%{_datadir}/man/*
/var/cache/fontconfig
%{_datadir}/fontconfig
%{_datadir}/xml/*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Thu Nov 24 2016 sulit <sulitsrc@163.com> - 2.12.1-2
- rebuild
- add buildrequires automake libtool

* Fri Oct 23 2015 cjacker - 2.11.94-6
- Rebuild for new 4.0 release

* Wed Mar 18 2009 Cjacker <cjacker@gmail.com>
- drop non-aa support
