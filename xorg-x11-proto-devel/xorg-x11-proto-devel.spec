# INFO: When doing a bootstrap build on a new architecture, set this to 1 to
# avoid build loops.
%define build_bootstrap 0

Summary: X.Org X11 Protocol headers
Name: xorg-x11-proto-devel
Version: 7.7
Release: 26
License: The Open Group License
Group: Development/System
URL: http://www.x.org

Source0:  http://xorg.freedesktop.org/archive/individual/proto//bigreqsproto-1.1.2.tar.bz2
Source1:  http://xorg.freedesktop.org/archive/individual/proto//compositeproto-0.4.2.tar.bz2
Source2:  http://xorg.freedesktop.org/archive/individual/proto//damageproto-1.2.1.tar.bz2
Source3:  http://xorg.freedesktop.org/archive/individual/proto//dmxproto-2.3.1.tar.bz2
Source4:  http://xorg.freedesktop.org/archive/individual/proto//dri2proto-2.8.tar.bz2
Source5:  http://xorg.freedesktop.org/archive/individual/proto//fixesproto-5.0.tar.bz2
Source6:  http://xorg.freedesktop.org/archive/individual/proto//fontsproto-2.1.3.tar.bz2
Source7:  http://xorg.freedesktop.org/archive/individual/proto//glproto-1.4.17.tar.bz2
Source8:  http://xorg.freedesktop.org/archive/individual/proto//inputproto-2.3.1.tar.bz2
Source9:  http://xorg.freedesktop.org/archive/individual/proto//kbproto-1.0.7.tar.bz2
Source10: http://xorg.freedesktop.org/archive/individual/proto//randrproto-1.5.0.tar.bz2
Source11: http://xorg.freedesktop.org/archive/individual/proto//recordproto-1.14.2.tar.bz2
Source12: http://xorg.freedesktop.org/archive/individual/proto//renderproto-0.11.1.tar.bz2
Source13: http://xorg.freedesktop.org/archive/individual/proto//resourceproto-1.2.0.tar.bz2
Source14: http://xorg.freedesktop.org/archive/individual/proto//scrnsaverproto-1.2.2.tar.bz2
Source15: http://xorg.freedesktop.org/archive/individual/proto//videoproto-2.3.2.tar.bz2
Source16: http://xorg.freedesktop.org/archive/individual/proto//xcmiscproto-1.2.2.tar.bz2
Source17: http://xorg.freedesktop.org/archive/individual/proto//xextproto-7.3.0.tar.bz2
Source18: http://xorg.freedesktop.org/archive/individual/proto//xf86bigfontproto-1.2.0.tar.bz2
Source19: http://xorg.freedesktop.org/archive/individual/proto//xf86dgaproto-2.1.tar.bz2
Source20: http://xorg.freedesktop.org/archive/individual/proto//xf86driproto-2.1.1.tar.bz2
Source21: http://xorg.freedesktop.org/archive/individual/proto//xf86vidmodeproto-2.3.1.tar.bz2
Source22: http://xorg.freedesktop.org/archive/individual/proto//xineramaproto-1.2.1.tar.bz2
Source23: http://xorg.freedesktop.org/archive/individual/proto//xproto-7.0.27.tar.bz2
Source24: http://xorg.freedesktop.org/archive/individual/proto//printproto-1.0.5.tar.bz2
Source25: http://xorg.freedesktop.org/archive/individual/proto//dri3proto-1.0.tar.bz2
Source26: http://xorg.freedesktop.org/archive/individual/proto//presentproto-1.0.tar.bz2
Source27: http://xorg.freedesktop.org/releases/individual/proto/xf86miscproto-0.9.3.tar.bz2
Source28: http://xorg.freedesktop.org/releases/individual/proto/evieext-1.1.1.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.0.2-1
# FIXME: This buildreq on xorg-x11-filesystem isn't really necessary, and
# can be removed in the future.  The main purpose of it being here right
# now, is to force buildmachines to get updated to solve the dir/symlink
# issue.
BuildRequires: xorg-x11-filesystem >= 0.99.2-3

Obsoletes: XFree86-devel, xorg-x11-devel

# NOTE: This dependency on xorg-x11-filesystem is required to work around
# a nasty upgrade problem when going from FC4->FC5 or monolithic to
# modular X.Org.  Bug #173384.
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

%description
X.Org X11 Protocol headers

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a26 -a27 -a28

%build
#ls -al

# Proceed through each proto package directory, building them all
for dir in $(ls -1) ; do
	pushd $dir
	%configure
	make %{?_smp_mflags}
	popd
done

%install
rm -rf $RPM_BUILD_ROOT
for dir in $(ls -1) ; do
	pushd $dir
	make install DESTDIR=$RPM_BUILD_ROOT
	popd
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_includedir}/*
%{_docdir}/*
%{_libdir}/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

