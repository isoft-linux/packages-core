Summary: X.Org X11 X server utilities
Name: xorg-x11-server-utils
Version: 1.1.1
Release: 5 
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org

Source0:  iceauth-1.0.7.tar.bz2
Source1:  rgb-1.0.6.tar.bz2
Source2:  sessreg-1.1.0.tar.bz2
Source3:  xcmsdb-1.0.5.tar.bz2
Source4:  xgamma-1.0.6.tar.bz2
Source5:  xhost-1.0.7.tar.bz2
Source6:  xmodmap-1.0.9.tar.bz2
Source7:  xrandr-1.4.3.tar.bz2
Source8:  xrdb-1.1.0.tar.bz2
Source9: xrefresh-1.0.5.tar.bz2
Source10: xset-1.2.3.tar.bz2
Source11: xauth-1.0.9.tar.bz2
Source12: xsetroot-1.1.1.tar.bz2
Source13: xstdcmap-1.0.3.tar.bz2
Source14: xvidtune-1.0.3.tar.bz2
Source15: xbacklight-1.2.1.tar.bz2
Source16: xinput-1.6.1.tar.bz2


Source100: mkxauth
Source101: mkxauth.man

Patch0: sessreg-fix-filenames.sed.patch

BuildRequires: pkgconfig
# xsetroot requires xbitmaps-devel
BuildRequires: xorg-x11-xbitmaps 
# xsetroot requires libX11-devel
BuildRequires: libX11-devel
# xsetroot requires libXmu-devel
BuildRequires: libXmu-devel
BuildRequires: libXrandr-devel
# FIXME: check if still needed for X11R7
Requires(pre): filesystem >= 2.3.7-1

# xrdb requires the C preprocessor to work properly

Provides: iceauth lbxproxy rgb sessreg xcmsdb xgamma xhost
Provides: xmodmap xrandr xrdb xrefresh xset xsetmode xsetpointer
Provides: xsetroot xstdcmap xvidtune xbacklight
Provides: xauth
# NOTE: iceauth, lbxproxy, rgb, sessreg, xcmsdb, xgamma, xhost, xmodmap,
# xrandr, xrdb, xrefresh, xset, xsetmode, xsetpointer, xsetroot, xstdcmap,
# xtrap, xvidtune, were all in xorg-x11 and XFree86 packages, so we obsolete
# them to ensure upgrades work.
Obsoletes: xorg-x11, XFree86

%description
A collection of utilities used to tweak and query the runtime configuration
of the X server.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16

pushd sessreg-1.1.0
%patch0 -p1
popd

%build
# Build all apps
{
   for app in * ; do
      pushd $app
      echo "******************** $app"
      %configure
      make %{?_smp_mflags}
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in * ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

# Install mkxauth
{
   install -m 755 %{SOURCE100} $RPM_BUILD_ROOT%{_bindir}/
   install -m 644 %{SOURCE101} $RPM_BUILD_ROOT%{_mandir}/man1/mkxauth.1x
}


rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/iceauth
%{_bindir}/sessreg
%{_bindir}/xcmsdb
%{_bindir}/xgamma
%{_bindir}/xhost
%{_bindir}/xinput
%{_bindir}/xmodmap
%{_bindir}/xrandr
%{_bindir}/xrdb
%{_bindir}/xkeystone
%{_bindir}/xrefresh
%{_bindir}/xset
%{_bindir}/xsetroot
%{_bindir}/xbacklight
%{_bindir}/xauth
%{_bindir}/mkxauth
%{_bindir}/showrgb
%{_bindir}/xstdcmap
%{_bindir}/xvidtune
%{_datadir}/X11/app-defaults/Xvidtune
%{_datadir}/X11/rgb.txt
%{_mandir}/man1/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

