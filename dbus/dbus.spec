%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global gettext_package         dbus-1

%global expat_version           1.95.5
%global libselinux_version      1.15.2

%global dbus_user_uid           81

%global dbus_common_config_opts --disable-libaudit --disable-selinux --with-system-socket=/run/dbus/system_bus_socket --with-system-pid-file=/run/dbus/messagebus.pid --with-dbus-user=dbus --libexecdir=/%{_libexecdir}/dbus-1 --docdir=%{_pkgdocdir} --enable-installed-tests

# Allow extra dependencies required for some tests to be disabled.
%bcond_with tests
# Disabled in June 2014: http://lists.freedesktop.org/archives/dbus/2014-June/016223.html
%bcond_with check

Name:    dbus
Epoch:   1
Version: 1.11.8
Release: 1%{?dist}
Summary: D-BUS message bus

# The effective license of the majority of the package, including the shared
# library, is "GPL-2+ or AFL-2.1". Certain utilities are "GPL-2+" only.
License: (GPLv2+ or AFL) and GPLv2+
URL:     http://www.freedesktop.org/Software/dbus/
#VCS:    git:git://git.freedesktop.org/git/dbus/dbus
Source0: http://dbus.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
Source1: 00-start-message-bus.sh

BuildRequires: libtool
BuildRequires: autoconf-archive
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: libX11-devel
BuildRequires: libcap-ng-devel
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(systemd)
BuildRequires: doxygen
# For building XML documentation.
BuildRequires: /usr/bin/xsltproc
BuildRequires: xmlto

#For macroized scriptlets.
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd

Requires:      dbus-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires(pre): /usr/sbin/useradd

# Note: These is only required for --with-tests; when bootstrapping, you can
# pass --without-tests.
%if %{with tests}
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: dbus-python
BuildRequires: pygobject3
%endif
%if %{with check}
BuildRequires: /usr/bin/Xvfb
%endif

%description
D-BUS is a system for sending messages between applications. It is
used both for the system-wide message bus service, and as a
per-user-login-session messaging facility.

%package libs
Summary: Libraries for accessing D-BUS

%description libs
This package contains lowlevel libraries for accessing D-BUS.

%package doc
Summary: Developer documentation for D-BUS
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
This package contains developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.

%package devel
Summary: Development files for D-BUS
# The server package can be a different architecture.
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains libraries and header files needed for
developing software that uses D-BUS.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%package x11
Summary: X11-requiring add-ons for D-BUS
# The server package can be a different architecture.
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: xorg-x11-xinit

%description x11
D-BUS contains some tools that require Xlib to be installed, those are
in this separate package so server systems need not install X.


%prep
%setup -q -n %{name}-%{version}


%build
# Avoid rpath.
if test -f autogen.sh; then env NOCONFIGURE=1 ./autogen.sh; else autoreconf --verbose --force --install; fi

mkdir build
pushd build
# See /usr/lib/rpm/macros
%global _configure ../configure
%configure %{dbus_common_config_opts} --enable-doxygen-docs --enable-xml-docs --disable-asserts
make V=1 %{?_smp_mflags}
popd

%if %{with check}
mkdir build-check
pushd build-check
%configure %{dbus_common_config_opts} --enable-asserts --enable-verbose-mode --enable-tests
make V=1 %{?_smp_mflags}
popd
%endif


%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot} INSTALL="install -p"
popd

find %{buildroot} -name '*.a' -type f -delete
find %{buildroot} -name '*.la' -type f -delete

install -Dp -m755 %{SOURCE1} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

mkdir -p %{buildroot}%{_datadir}/dbus-1/interfaces

# Make sure that when somebody asks for D-Bus under the name of the
# old SysV script, that he ends up with the standard dbus.service name
# now.
ln -s dbus.service %{buildroot}%{_unitdir}/messagebus.service

## %find_lang %{gettext_package}
# Delete the old legacy sysv init script
rm -rf %{buildroot}%{_initrddir}

mkdir -p %{buildroot}/var/lib/dbus

install -pm 644 -t %{buildroot}%{_pkgdocdir} \
    doc/introspect.dtd doc/introspect.xsl doc/system-activation.txt

# Make sure that the documentation shows up in Devhelp.
mkdir -p %{buildroot}%{_datadir}/gtk-doc/html
ln -s %{_pkgdocdir} %{buildroot}%{_datadir}/gtk-doc/html/dbus

# Shell wrapper for installed tests, modified from Debian package.
cat > dbus-run-installed-tests <<EOF
#!/bin/sh
# installed-tests wrapper for dbus. Outputs TAP format because why not

set -e

timeout="timeout 300s"
ret=0
i=0
tmpdir=\$(mktemp --directory --tmpdir dbus-run-installed-tests.XXXXXX)

for t in %{_libexecdir}/dbus-1/installed-tests/dbus/test-*; do
    i=\$(( \$i + 1 ))
    echo "# \$i - \$t ..."
    echo "x" > "\$tmpdir/result"
    ( set +e; \$timeout \$t; echo "\$?" > "\$tmpdir/result" ) 2>&1 | sed 's/^/# /'
    e="\$(cat "\$tmpdir/result")"
    case "\$e" in
        (0)
            echo "ok \$i - \$t"
            ;;
        (77)
            echo "ok \$i # SKIP \$t"
            ;;
        (*)
            echo "not ok \$i - \$t (\$e)"
            ret=1
            ;;
    esac
done

rm -rf tmpdir
echo "1..\$i"
exit \$ret
EOF

install -pm 755 -t %{buildroot}%{_libexecdir}/dbus-1 dbus-run-installed-tests


%if %{with check}
%check
pushd build-check

# TODO: better script for this...
export DISPLAY=42
{ Xvfb :${DISPLAY} -nolisten tcp -auth /dev/null >/dev/null 2>&1 &
  trap "kill -15 $! || true" 0 HUP INT QUIT TRAP TERM; };
if ! env DBUS_TEST_SLOW=1 make check; then
    echo "Tests failed, finding all Automake logs..." 1>&2;
    find . -type f -name '*.trs' | while read trs; do cat ${trs}; cat ${trs%%.trs}.log; done
    echo  "Exiting abnormally due to make check failure above" 1>&2;
    exit 1;
fi
popd
%endif


%pre
# Add the "dbus" user and group
/usr/sbin/groupadd -r -g %{dbus_user_uid} dbus 2>/dev/null || :
/usr/sbin/useradd -c 'System message bus' -u %{dbus_user_uid} -g %{dbus_user_uid} \
    -s /sbin/nologin -r -d '/' dbus 2> /dev/null || :

%post libs -p /sbin/ldconfig

%preun
%systemd_preun stop dbus.service dbus.socket

%postun libs -p /sbin/ldconfig

%postun
%systemd_postun


%files
# Strictly speaking, we could remove the COPYING from this subpackage and 
# just have it be in libs, because dbus Requires dbus-libs.
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog HACKING NEWS README
%exclude %{_pkgdocdir}/api
%exclude %{_pkgdocdir}/dbus.devhelp
%exclude %{_pkgdocdir}/diagram.*
%exclude %{_pkgdocdir}/introspect.*
%exclude %{_pkgdocdir}/system-activation.txt
%exclude %{_pkgdocdir}/*.html
%dir %{_sysconfdir}/dbus-1
%config %{_sysconfdir}/dbus-1/session.conf
%config %{_sysconfdir}/dbus-1/system.conf
%ghost %dir /run/%{name}
%dir %{_localstatedir}/lib/dbus/
%{_bindir}/dbus-daemon
%{_bindir}/dbus-send
%{_bindir}/dbus-cleanup-sockets
%{_bindir}/dbus-run-session
%{_bindir}/dbus-monitor
%{_bindir}/dbus-test-tool
%{_bindir}/dbus-update-activation-environment
%{_bindir}/dbus-uuidgen
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-run-session.1*
%{_mandir}/man1/dbus-monitor.1*
%{_mandir}/man1/dbus-send.1*
%{_mandir}/man1/dbus-test-tool.1*
%{_mandir}/man1/dbus-update-activation-environment.1*
%{_mandir}/man1/dbus-uuidgen.1*
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/session.conf
%{_datadir}/dbus-1/system.conf
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/interfaces
%dir %{_libexecdir}/dbus-1
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,dbus) %{_libexecdir}/dbus-1/dbus-daemon-launch-helper
%exclude %{_libexecdir}/dbus-1/dbus-run-installed-tests
%{_unitdir}/dbus.service
%{_unitdir}/dbus.socket
%{_unitdir}/messagebus.service
%{_unitdir}/multi-user.target.wants/dbus.service
%{_unitdir}/sockets.target.wants/dbus.socket

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/*dbus-1*.so.*

%files tests
%{_libexecdir}/dbus-1/installed-tests
%{_libexecdir}/dbus-1/dbus-run-installed-tests
%{_datadir}/installed-tests

%files x11
%{_bindir}/dbus-launch
%{_mandir}/man1/dbus-launch.1*
%{_sysconfdir}/X11/xinit/xinitrc.d/00-start-message-bus.sh

%files doc
%{_pkgdocdir}/*
%{_datadir}/gtk-doc
%exclude %{_pkgdocdir}/AUTHORS
%exclude %{_pkgdocdir}/ChangeLog
%exclude %{_pkgdocdir}/HACKING
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README

%files devel
%{_libdir}/lib*.so
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/
%{_libdir}/pkgconfig/dbus-1.pc
%{_includedir}/*


%changelog
* Wed Dec 07 2016 sulit - 1:1.11.8-1
- upgrade dbus to 1.11.8
- add buildrequire autoconf-archive

* Thu Dec 31 2015 Cjacker <cjacker@foxmail.com> - 1:1.11.0-2
- Update

* Fri Oct 23 2015 cjacker - 1:1.9.20-3
- Rebuild for new 4.0 release

* Sun Aug 23 2015 Cjacker <cjacker@foxmail.com>
- update to 1.9.20
