#NOTE: localuser.sh
#Networkmanager will change hostname, without this scripts, after hostname changed, all x clients will failed to find a display.(xauth failed)


%define pkgname xinit

Summary:    X.Org X11 X Window System xinit startup scripts
Name:       xorg-x11-%{pkgname}
Version:    1.3.4
Release:    11%{?dist}
License:    MIT
URL:        http://www.x.org

Source0:    http://xorg.freedesktop.org/archive/individual/app/%{pkgname}-%{version}.tar.bz2
Source10:   xinitrc-common
Source11:   xinitrc
Source12:   Xclients
Source13:   Xmodmap
Source14:   Xresources
# NOTE: Xsession is used by xdm/kdm/gdm and possibly others, so we keep it
#       here instead of the xdm package.
Source16:   Xsession
Source17:   localuser.sh
Source18:   xinit-compat.desktop
Source19:   xinit-compat

# Fedora specific patches
Patch1: xinit-1.0.2-client-session.patch
# This is the Xserver default starting at xorg-x11-server >= 1.17, drop once
# we've that version, rhbz#1111684
Patch2: 0001-startx-Pass-nolisten-tcp-by-default.patch
# A few fixes submitted upstream, rhbz#1177513, rhbz#1203780
Patch3: 0001-startx-Pass-keeptty-when-telling-the-server-to-start.patch
Patch4: 0002-startx-Fix-startx-picking-an-already-used-display-nu.patch
Patch5: 0003-startx-Make-startx-auto-display-select-work-with-per.patch
# Fedora specific patch to match the similar patch in the xserver
Patch6: xinit-1.3.4-set-XORG_RUN_AS_USER_OK.patch

BuildRequires:  pkgconfig(x11)
BuildRequires:  dbus-devel

# NOTE: startx needs xauth in order to run, but that is not picked up
#       automatically by rpm.  (Bug #173684)
Requires:   xorg-x11-server-utils
# next two are for localuser.sh
Requires:   coreutils
Requires:   xhost

Provides:   %{pkgname} = %{version}

%description
X.Org X11 X Window System xinit startup scripts.

%package session
Summary:    Display manager support for ~/.xsession and ~/.Xclients

%description session
Allows legacy ~/.xsession and ~/.Xclients files to be used from display
managers.

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install
install -p -m644 -D %{SOURCE18} $RPM_BUILD_ROOT%{_datadir}/xsessions/xinit-compat.desktop

# Install Red Hat custom xinitrc, etc.
{
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit

    install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc-common

    for script in %{SOURCE11} %{SOURCE12} %{SOURCE16} ; do
        install -p -m 755 $script $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/${script##*/}
    done

    install -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xmodmap
    install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xresources

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
    install -p -m 755 %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/localuser.sh

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/Xclients.d

    mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
    install -p -m 755 %{SOURCE19} $RPM_BUILD_ROOT%{_libexecdir}
}

%files
%doc COPYING README ChangeLog
%{_bindir}/startx
%{_bindir}/xinit
%dir %{_sysconfdir}/X11/xinit
%{_sysconfdir}/X11/xinit/xinitrc
%{_sysconfdir}/X11/xinit/xinitrc-common
%config(noreplace) %{_sysconfdir}/X11/Xmodmap
%config(noreplace) %{_sysconfdir}/X11/Xresources
%dir %{_sysconfdir}/X11/xinit/Xclients.d
%{_sysconfdir}/X11/xinit/Xclients
%{_sysconfdir}/X11/xinit/Xsession
%dir %{_sysconfdir}/X11/xinit/xinitrc.d
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*

%files session
%{_libexecdir}/xinit-compat
%{_datadir}/xsessions/xinit-compat.desktop

%changelog
* Fri Oct 23 2015 cjacker - 1.3.4-11
- Rebuild for new 4.0 release

