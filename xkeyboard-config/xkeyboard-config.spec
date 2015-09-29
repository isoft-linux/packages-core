Summary: xkeyboard-config alternative xkb data files
Name: xkeyboard-config
Version: 2.15
Release: 1
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source0: http://ftp.x.org/pub/individual/data/xkeyboard-config/xkeyboard-config-%{version}.tar.bz2
BuildArch: noarch

BuildRequires: pkgconfig
BuildRequires: intltool
BuildRequires: perl-XML-Parser

Provides: xkbdata
Provides: xkeyboard-config
Provides: xorg-x11-xkbdata
Provides: %{name}-devel

%description
xkeyboard-config alternative xkb data files

%prep
%setup -q 
%build
%configure \
    --disable-runtime-deps \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --with-xkb-rules-symlink=xorg 

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Remove unnecessary symlink
rm -f $RPM_BUILD_ROOT%{_datadir}/X11/xkb/compiled

# Create filelist
{
   FILESLIST=${PWD}/files.list
   pushd $RPM_BUILD_ROOT
   find ./usr/share/X11 -type d | sed -e "s/^\./%dir /g" > $FILESLIST
   find ./usr/share/X11 -type f | sed -e "s/^\.//g" >> $FILESLIST
   popd
}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f files.list -f %{name}.lang
%defattr(-,root,root,-)
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml
%{_datadir}/pkgconfig/*.pc
%{_mandir}/man7/xkeyboard-config.7.gz

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

