# Only enable if using patches that touches configure.ac,
# Makefile.am or other build system related files
#
#define enable_autoreconf 1

Summary: An authorization framework
Name: polkit
Version: 0.113
Release: 2%{?dist}
License: LGPLv2+
URL: http://www.freedesktop.org/wiki/Software/polkit
Source0: http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Source1: http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz.sign
BuildRequires: glib2-devel >= 2.30.0
BuildRequires: expat-devel
BuildRequires: pam-devel
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: systemd, systemd-devel
BuildRequires: mozjs17-devel

%if 0%{?enable_autoreconf}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
%endif

Requires: dbus, polkit-pkla-compat

Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig, systemd
Requires(preun): systemd
Requires(postun): /sbin/ldconfig, systemd

Obsoletes: PolicyKit <= 0.10
Provides: PolicyKit = 0.11

# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts: polkit-gnome < 0.97

Obsoletes: polkit-desktop-policy < 0.103
Provides: polkit-desktop-policy = 0.103

Obsoletes: polkit-js-engine < 0.110-4
Provides: polkit-js-engine = %{version}-%{release}

%description
polkit is a toolkit for defining and handling authorizations.  It is
used for allowing unprivileged processes to speak to privileged
processes.

%package devel
Summary: Development files for polkit
Requires: %name = %{version}-%{release}
Requires: %name-docs = %{version}-%{release}
Requires: glib2-devel
Obsoletes: PolicyKit-devel <= 0.10
Provides: PolicyKit-devel = 0.11

%description devel
Development files for polkit.

%package docs
Summary: Development documentation for polkit
Requires: %name-devel = %{version}-%{release}
Obsoletes: PolicyKit-docs <= 0.10
Provides: PolicyKit-docs = 0.11
BuildArch: noarch

%description docs
Development documentation for polkit.

%package libs
Summary: Libraries for polkit

%description libs
Libraries files for polkit.


%prep
%setup -q

%build
%if 0%{?enable_autoreconf}
autoreconf -i
%endif
# we can't use _hardened_build here, see
# https://bugzilla.redhat.com/show_bug.cgi?id=962005
export CFLAGS='-fPIC %optflags'
export LDFLAGS='-pie -Wl,-z,now -Wl,-z,relro'
%configure --enable-gtk-doc \
        --disable-static \
        --enable-introspection \
        --disable-examples \
        --enable-libsystemd-login=yes --with-mozjs=mozjs-17.0
make V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang polkit-1

%pre
getent group polkitd >/dev/null || groupadd -r polkitd
getent passwd polkitd >/dev/null || useradd -r -g polkitd -d / -s /sbin/nologin -c "User for polkitd" polkitd
exit 0

%post
# The implied (systemctl preset) will fail and complain, but the macro hides
# and ignores the fact.  This is in fact what we want, polkit.service does not
# have an [Install] section and it is always started on demand.
%systemd_post polkit.service

%preun
%systemd_preun polkit.service

%postun
%systemd_postun_with_restart polkit.service

%files -f polkit-1.lang
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_datadir}/man/man1/*
%{_datadir}/man/man8/*
%{_datadir}/dbus-1/system-services/*
%{_unitdir}/polkit.service
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%attr(0700,polkitd,root) %dir %{_datadir}/polkit-1/rules.d
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%dir %{_sysconfdir}/polkit-1
%{_sysconfdir}/polkit-1/rules.d/50-default.rules
%attr(0700,polkitd,root) %dir %{_sysconfdir}/polkit-1/rules.d
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%dir %{_prefix}/lib/polkit-1
%{_prefix}/lib/polkit-1/polkitd

# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_prefix}/lib/polkit-1/polkit-agent-helper-1

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_includedir}/*

%files docs
%defattr(-,root,root,-)
%{_datadir}/gtk-doc

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/*.typelib

%changelog
* Fri Oct 23 2015 cjacker - 0.113-2
- Rebuild for new 4.0 release

