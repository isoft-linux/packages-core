Summary:    X.Org X11 twm window manager
Name:       xorg-x11-twm
# NOTE: Remove Epoch line if package gets renamed to something like "twm"
Epoch:      1
Version:    1.0.9
Release:    3%{?dist}
License:    MIT
URL:        http://www.x.org

Source0:    ftp://ftp.x.org/pub/individual/app/twm-%{version}.tar.bz2

BuildRequires:  bison
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xproto) >= 7.0.17
BuildRequires:  pkgconfig(xt)

Requires:       xterm
Provides:       twm = %{epoch}:%{version}

%description
X.Org X11 Tab Window Manager.

%prep
%setup -q -n twm-%{version}

%build
autoreconf -v --install
%configure 
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# FIXME: Upstream sources do not create the system wide twm config dir, nor
# install the default config file currently.  We'll work around it here for now.
{
   echo "FIXME: Upstream doesn't install systemwide config by default"
   mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/twm
   install -p -m 0644 src/system.twmrc $RPM_BUILD_ROOT%{_sysconfdir}/X11/twm/
   rm -fr $RPM_BUILD_ROOT%{_datadir}/X11
}

%files
%doc COPYING ChangeLog
%{_bindir}/twm
%{_mandir}/man1/twm.1*
%dir %{_sysconfdir}/X11/twm
%config %{_sysconfdir}/X11/twm/system.twmrc

%changelog
* Fri Oct 23 2015 cjacker - 1:1.0.9-3
- Rebuild for new 4.0 release

* Thu Jul 16 2015 Cjacker <cjacker@foxmail.com>
- build, as the fallback wm to deal with emergency statuation.
