%define pkgname xkb-utils

Summary: X.Org X11 xkb utilities
Name: xorg-x11-%{pkgname}
Version: 7.7 
Release: 3.1 
License: MIT/X11
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%define xorgurl http://xorg.freedesktop.org/releases/X11R7.0-RC4/everything
Source0: %{xorgurl}/xkbutils-1.0.4.tar.bz2
Source1: %{xorgurl}/xkbcomp-1.3.0.tar.bz2
Source2: %{xorgurl}/xkbevd-1.1.4.tar.bz2
Source4: %{xorgurl}/setxkbmap-1.3.1.tar.bz2

BuildRequires: pkgconfig
BuildRequires: libxkbfile-devel
BuildRequires: libX11-devel
BuildRequires: libXaw-devel
BuildRequires: libXt-devel
BuildRequires: libXext-devel
BuildRequires: libXpm-devel

Provides: setxkbmap, xkbcomp, xkbevd, xkbutils
Obsoletes: XFree86, xorg-x11

%description
X.Org X11 xkb utilities

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a4

%build
# Build everything
{
   for pkg in xkbutils setxkbmap xkbcomp xkbevd ; do
      pushd $pkg-*
      %configure
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT

# Install everything
{
   for pkg in xkbutils setxkbmap xkbcomp xkbevd ; do
      pushd $pkg-*
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%dir %{_bindir}
%{_bindir}/setxkbmap
%{_bindir}/xkbbell
%{_bindir}/xkbcomp
%{_bindir}/xkbevd
%{_bindir}/xkbvleds
%{_bindir}/xkbwatch
%dir %{_mandir}
%{_mandir}/man1
%{_libdir}/pkgconfig/*

%changelog
* Fri Oct 23 2015 cjacker - 7.7-3.1
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

