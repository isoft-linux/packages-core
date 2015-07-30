%define pkgname fonts-utils

# NOTE: When enabled, this provides symbolic links in /usr/X11R6/bin which
# provide backward compatibility for utilities/scripts that hard code paths
# to /usr/X11R6/bin/mkfontdir et al.  This compatibility support will be
# disabled and removed in a future OS release, so 3rd party application
# developers and package maintainers should update their software as soon
# as possible.
%define with_X11R6_compat 1
%define _x11r6bindir /usr/X11R6/bin

Summary: X.Org X11 font utilities
Name: xorg-x11-%{pkgname}
# IMPORTANT: If package ever gets renamed to something else, remove the Epoch line!
Epoch: 1
Version: 1.1.1
Release: 3
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org

Source0: http://xorg.freedesktop.org/releases/X11R7.0/src/everything/bdftopcf-1.0.5.tar.bz2
Source1: http://xorg.freedesktop.org/releases/X11R7.0/src/everything/fonttosfnt-1.0.1.tar.bz2
Source2: http://xorg.freedesktop.org/releases/X11R7.0/src/everything/mkfontdir-1.0.7.tar.bz2
Source3: http://xorg.freedesktop.org/releases/X11R7.0/src/everything/mkfontscale-1.1.2.tar.bz2
Source4: font-util-1.3.1.tar.bz2 
Patch:   font-util-fix.patch 
Patch1:	fonttosfnt-fix-freetype-22.patch
BuildRequires: pkgconfig
# xorg-x11-libXfont-devel needed for bdftopcf
BuildRequires: libXfont-devel
# xorg-x11-libX11-devel needed for fonttosfnt
BuildRequires: libX11-devel
# xorg-x11-libfontenc-devel needed for fonttosfnt, mkfontscale
BuildRequires: libfontenc-devel >= 0.99.2-2
# freetype-devel needed for bdftopcf, fonttosfnt, mkfontscale
BuildRequires: freetype-devel
# zlib-devel needed for bdftopcf
BuildRequires: zlib-devel
# xorg-x11-proto-devel is needed for mkfontscale, which includes headers
# from it directly.
BuildRequires: xorg-x11-proto-devel

BuildRequires: autoconf

Requires(pre): xorg-x11-filesystem >= 0.99.2-3

# NOTE: This versioned pre-dependency is needed to ensure that the bugfix for
# bug #173875 is installed in order for mkfontscale/mkfontdir to work
# properly.  It is a "pre" dep, to ensure libfontenc gets installed before
# xorg-font-utils, before any fonts in an rpm upgrade or multi-transaction
# set, avoiding a possible race condition.
Requires(pre): libfontenc >= 0.99.2-2


Provides: %{pkgname}
Provides: xorg-x11-font-utils
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, bdftruncate, ucs2any
# NOTE: XFree86-font-utils package contains mkfontdir, mkfontscale, so this
# is needed for upgrades to work properly from OS releases that had XFree86
Obsoletes: XFree86-font-utils
# NOTE: XFree86 package used to contain bdftopcf, so this is needed for
# upgrades to work.  It also contained mkfontdir/mkfontscale at one point,
# so we just Conflict without a version specification.
Conflicts: XFree86
# NOTE: The fonts/util subdir moved from xorg-x11-base-fonts to
# xorg-x11-font-utils in 6.7.99.903-3
Obsoletes: xorg-x11-base-fonts <= 6.7.99.903-3
# NOTE: ucs2any moved from xorg-x11-tools to xorg-x11-font-utils in 6.7.99.903-3
Obsoletes: xorg-x11-tools <= 6.7.99.903-3

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
%patch1 -p1
%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      pushd $app-*
      # FIXME: We run autoconf to activate font-util-0.99.1-mapdir-use-datadir-fix.patch
      case $app in
         font-util)
            autoconf
            ;;
      esac
      %configure
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
      pushd $app-*
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%if %{with_X11R6_compat}
{
   mkdir -p $RPM_BUILD_ROOT%{_x11r6bindir}

   for util in mkfontdir mkfontscale ; do
      ln -sf ../../..%{_bindir}/$util $RPM_BUILD_ROOT%{_x11r6bindir}/$util
   done
}
%endif
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# FIXME: Include missing docs sometime
%doc
%{_bindir}/bdftopcf
%{_bindir}/bdftruncate
%{_bindir}/fonttosfnt
%{_bindir}/mkfontdir
%{_bindir}/mkfontscale
%{_bindir}/ucs2any
# NOTE: These compat symlinks will be removed in a future OS release.
# Developers and package maintainers should update their software to handle
# the X11R7 changes in a clean manner.
%if %{with_X11R6_compat}
%dir %{_x11r6bindir}
%{_x11r6bindir}/mkfontdir
%{_x11r6bindir}/mkfontscale
%endif
%{_datadir}/fonts/X11/util/map-*
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
#%dir %{_mandir}/man1x
%{_mandir}/man1

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

