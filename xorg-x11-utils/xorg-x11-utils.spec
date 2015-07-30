Summary: X.Org X11 X client utilities
Name: xorg-x11-utils
Version: 1.1.1
Release: 6 
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org

Source0:  xdpyinfo-1.3.2.tar.bz2
Source1:  xev-1.2.2.tar.bz2
Source2:  xlsatoms-1.1.2.tar.bz2
Source3:  xlsclients-1.1.3.tar.bz2
Source4:  xprop-1.2.2.tar.bz2
Source5:  xvinfo-1.1.3.tar.bz2
Source6: xwininfo-1.1.3.tar.bz2 
Source7: xkill-1.0.4.tar.bz2
Source8: luit-1.1.1.tar.bz2
Source9: xmessage-1.0.4.tar.bz2

Patch0: luit-git-fixes.patch

BuildRequires: pkgconfig

BuildRequires: libXv-devel, libXft-devel

Provides: xdpyinfo xev xfd xlsatoms xlsclients xlsfonts xprop xvinfo xwininfo xmessage luit

%description
A collection of client utilities which can be used to query the X server
for various information, view and select fonts, etc.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9

pushd luit-1.1.1
%patch0 -p1
popd

%build
pushd luit-1.1.1
autoreconf -ivf
popd

# Build all apps
{
   for app in * ; do
      pushd $app
      %configure
      make
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
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/luit
%{_bindir}/xmessage
%{_bindir}/xdpyinfo
%{_bindir}/xev
%{_bindir}/xlsatoms
%{_bindir}/xlsclients
%{_bindir}/xkill
%{_bindir}/xprop
%{_bindir}/xvinfo
%{_bindir}/xwininfo
%{_datadir}/X11/app-defaults/Xmessage
%{_datadir}/X11/app-defaults/Xmessage-color
%{_mandir}/man1/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

