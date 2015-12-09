%define pkgname xorg-server

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#below definations should always match to xorg-server.pc
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 20 
%global videodrv_minor 0
%global xinput_major 22
%global xinput_minor 1
%global extension_major 9
%global extension_minor 0

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   1.18.0
Release:   6
URL:       http://www.x.org
License:   MIT

Source0:   http://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2

Source4:   10-quirks.conf 


Source10:   xserver.pamd

# "useful" xvfb-run script
Source20:  http://svn.exactcode.de/t2/trunk/package/xorg/xorg-server/xvfb-run.sh

# for ABI requires generation in drivers
Source30: xserver-sdk-abi-requires.release

Patch0:  autoconfig-sis.patch
Patch1:  autoconfig-nvidia.patch
Patch10: xorg-x11-extramodes.patch

# Trivial things to never merge upstream ever:
# This really could be done prettier.
Patch5002: xserver-1.4.99-ssh-isnt-local.patch
Patch7025: 0001-Always-install-vbe-and-int10-sdk-headers.patch
# do not upstream - do not even use here yet
Patch7027: xserver-autobind-hotplug.patch
# because the display-managers are not ready yet, do not upstream
Patch10000: 0001-hack-Make-the-suid-root-wrapper-always-start-.patch
# Fix build with gcc5, submitted upstream, likely needs a better fix
Patch10001: 0001-sdksyms.sh-Make-sdksyms.sh-work-with-gcc5.patch
Patch10003: 0001-include-Fix-endianness-setup.patch
Patch10004: 0001-Xorg.wrap-activate-libdrm-based-detection-for-KMS-dr.patch


#backport from post 1.18
Patch20000: 0001-also-dump-passive-grubs-on-XF86LogGrabInfo.patch
Patch20001: 0002-glamor-avoid-GL-errors-from-mapping-with-size-0.patch
Patch20002: 0003-glamor-handle-GL_OUT_OF_MEMORY-when-allocating-texture-image.patch
Patch20003: 0004-glamor-fix-crashes-when-glyph-atlas-allocation-fails.patch
Patch20004: 0005-glamor-fix-rendering-when-core-font-texture-allocation-fails.patch
Patch20005: 0006-glamor-fix-assert-failure-when-fallback-picture-upload-alloc-fails.patch
Patch20006: 0007-glamor-fix-segfault-in-fallback-picture-uploading.patch
Patch20007: 0008-glamor-no-need-to-glflush-before-destroying-pixmap.patch
Patch20008: 0009-modesetting-No-need-to-free-the-EGLImage-just-before-freeing-the-pixmap.patch
Patch20009: 0010-glamor-remove-glamor_egl_destroy_textured_pixmap.patch
Patch20010: 0011-glamor-unexport-glamor_destroy_textured_pixmap.patch
Patch20011: 0012-glamor-hook-up-EGL-DestroyPixmap-through-normal-wrap-chain.patch
Patch20012: 0013-glamor-use-gbm-function-for-get-FD-from-GBM-BO.patch
Patch20013: 0014-glamor-use-real-types-for-glamor_egl-public-gbm-functions.patch
Patch20014: 0015-glamor-simplify-DRI3-pixmap-from-fd-using-GBM.patch
Patch20015: 0016-glamor-make-glamor_get_name_from_bo-static.patch
Patch20016: 0017-glamor-delay-making-pixmaps-shareable-util-we-need-to.patch

Patch20017: 0018-fix-minor-memory-leak.patch
Patch20018: 0019-Split-filter-execution-into-separate-function.patch
Patch20019: 0020-input-add-deviceEventSource-enum.patch
Patch20020: 0021-input-add-focus-in-event-source.patch
Patch20021: 0022-xwayland-use-focusin-events-for-keyboard-enter.patch
Patch20022: 0023-xnest-fix-needless-build-dependency-on-xcb-util-keysyms.patch
Patch20023: 0024-dix-remove-redundant-ChangeWindowProperty.patch
Patch20024: 0025-kdrive-fix-off-by-one.patch
Patch20025: 0026-replace-sun-with__sun.patch
Patch20026: 0027-xwayland-fix-memleak-on-error-path-in-xwl_realize_window.patch
Patch20027: 0028-xwayland-check-if-xwl_output-succeeded.patch
Patch20028: 0029-xwayland-do-not-set-root-clip-when-rootless.patch
Patch20029: 0030-xwayland-always-update-the-wl_pointer-cursor-on-pointer-focus.patch
Patch20030: 0031-xwayland-update-screen-size-on-output-removal.patch

Patch20031: 0008-x86emu-correctly-handle-0x66-prefix-for-some-instruction.patch
Patch20032: 0056-x86emu-squash-a-warning.patch
Patch20033: 0009-remove-non-smart-scheduler-do-not-require-setitimer.patch
Patch20034: 0010-render-use-ostimer-for-animated-cursor-timing.patch
Patch20035: 0011-dix-move-initfonts-up-above-screen-initialization.patch

Patch20040: 0040-os-add-nofityfd-interfaces.patch
Patch20041: 0041-os-implement-support-for-notifyfd-X_NOTIFY_WRITE.patch
Patch20042: 0042-config-use-NotifyFd-for-dbus-interface.patch
Patch20043: 0043-config-use-NotifyFd-interface-for-udev.patch
Patch20044: 0044-hw-kdrive-use-NotifyFd-interface-for-kdrive-linux-APM-monitoring.patch
Patch20045: 0045-hw-kdrive-use-NotifyFd-for-kdrive-input-devices.patch
Patch20046: 0046-kdrive-ephyr-use-NotifyFd-for-XCB-connection-input.patch
Patch20047: 0047-modesettings-use-NotifyFd-for-drm-event-monitoring.patch
Patch20048: 0048-hw-xwayland-use-NotifyFd-handler-to-monitor-wayland-socket.patch
Patch20049: 0049-xext-xselinux-use-NotifyFd.patch
Patch20050: 0050-os-xdmcp-replace-xdmcp-block-wakeup-handlers-with-timer-and-NotifyFd.patch
Patch20051: 0051-os-use-NotifyFd-interface-for-listen-descriptors.patch
Patch20052: 0052-modesetting-drop-platform_dev-pointer.patch
Patch20053: 0053-present-requery-pending-flips-with-the-right-sync_flip-mode.patch
Patch20054: 0054-present-when-cancelling-pending-sync-flip-requeue-it.patch
Patch20055: 0055-present-do-not-replace-pixmaps-on-redirected-window-on-unflip.patch


BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: xcb-util
BuildRequires: xcb-util-wm-devel
BuildRequires: xorg-x11-proto-devel >= 7.3-10
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-3
BuildRequires: libXfont-devel libXau-devel libxkbfile-devel libXres-devel
BuildRequires: libfontenc-devel libXtst-devel libXdmcp-devel
BuildRequires: libX11-devel libXext-devel
BuildRequires: libXft libXinerama libXcursor
BuildRequires: libXt-devel libdmx-devel libXmu-devel libXrender-devel
BuildRequires: libXi-devel libXpm-devel libXaw-devel libXfixes-devel
#autoreconf need it
BuildRequires: xorg-x11-font-utils
BuildRequires: libXv-devel libxshmfence-devel
BuildRequires: libepoxy-devel
BuildRequires: pixman-devel libpciaccess-devel byacc flex
BuildRequires: mesa-libGL-devel mesa-libEGL-devel 
BuildRequires: mesa-libgbm-devel
BuildRequires: nettle-devel
BuildRequires: libdrm-devel kernel-devel
BuildRequires: dbus-devel
BuildRequires: tslib-devel
BuildRequires: systemd-devel
BuildRequires: libxcb-devel xcb-util-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-renderutil-devel xcb-util-wm-devel
BuildRequires: libwayland-client-devel libwayland-server-devel
BuildRequires: gawk make doxygen xmlto libxslt flex bison gdbm-devel kernel-headers
BuildRequires: libgcrypt-devel openssl-devel 
Requires: libdrm 

%description
X.Org X11 X server

%package common
Summary: Xorg server common files

%description common
Common files shared among all X servers.

%package Xorg
Summary: Xorg X server
Provides: Xorg = %{version}-%{release}
Provides: Xserver
# Requires: xorg-x11-drivers >= 0.99.2-4
Requires: xorg-x11-xkb-utils
Requires: xorg-x11-server-utils
Requires: xorg-x11-xkbdata 
Requires: xorg-x11-server-common >= %{version}-%{release}

Provides: xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides: xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides: xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides: xserver-abi(extension-%{extension_major}) = %{extension_minor}

# These drivers were dropped in F7 for being broken, so uninstall them.
Obsoletes: xorg-x11-drv-elo2300 <= 1.1.0-2.fc7
Obsoletes: xorg-x11-drv-joystick <= 1.1.0-2.fc7
# Dropped from F9 for being broken, uninstall it.
Obsoletes: xorg-x11-drv-magictouch <= 1.0.0.5-5.fc8
# Force sufficiently new libpciaccess
Conflicts: libpciaccess < 0.9.1-2

%description Xorg
X.org X11 is an open source implementation of the X Window System.  It
provides the basic low level functionality which full fledged
graphical user interfaces (GUIs) such as GNOME and KDE are designed
upon.


%package suid 
Summary: SUID wrapper of X
Requires: xorg-x11-server-common >= %{version}-%{release}

%description suid
SUID wrapper of X

%package Xnest
Summary: A nested server.
Obsoletes: xorg-x11-Xnest
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xnest

%description Xnest
Xnest is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.


%package Xdmx
Summary: Distributed Multihead X Server and utilities
Obsoletes: xorg-x11-Xdmx
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xdmx

%description Xdmx
Xdmx is proxy X server that provides multi-head support for multiple displays
attached to different machines (each of which is running a typical X server).
When Xinerama is used with Xdmx, the multiple displays on multiple machines
are presented to the user as a single unified screen.  A simple application
for Xdmx would be to provide multi-head support using two desktop machines,
each of which has a single display device attached to it.  A complex
application for Xdmx would be to unify a 4 by 4 grid of 1280x1024 displays
(each attached to one of 16 computers) into a unified 5120x4096 display.


%package Xvfb
Summary: A X Windows System virtual framebuffer X server.
Obsoletes: xorg-x11-Xvfb
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xvfb

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on
machines with no display hardware and no physical input devices.
Xvfb simulates a dumb framebuffer using virtual memory.  Xvfb does
not open any devices, but behaves otherwise as an X display.  Xvfb
is normally used for testing servers.


%package Xwayland
Summary: X Clients under Wayland (XWayland)
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xwayland

%description Xwayland
X Clients under Wayland (XWayland)

%package Xephyr
Summary: A nested server.
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xephyr

%description Xephyr
Xephyr is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.  Unlike
Xnest, Xephyr renders to an X image rather than relaying the
X protocol, and therefore supports the newer X extensions like
Render and Composite.


%package devel
Summary: SDK for X server driver module development
Obsoletes: xorg-x11-sdk xorg-x11-server-sdk
Requires: xorg-x11-util-macros
Requires: xorg-x11-proto-devel
Requires: pkgconfig pixman-devel libpciaccess-devel
Requires(pre): xorg-x11-filesystem >= 0.99.2-3
Provides: libxf86config-devel = %{version}-%{release}
# Virtual provide for transition.  Delete me someday.
Provides: xorg-x11-server-sdk = %{version}-%{release}

Provides: glamor-egl-devel
Provides: glamor-devel
Obsoletes: glamor-egl-devel
Obsoletes: glamor-devel


%description devel
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.


%define moduledir	%{_libdir}/xorg/modules
%define sdkdir		%{_includedir}/xorg

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p0
%patch1 -p1
%patch10 -p1

%patch5002 -p1

%patch7025 -p1
%patch7027 -p1
%patch10000 -p1
%patch10001 -p1
%patch10003 -p1
%patch10004 -p1


%patch20000 -p1
%patch20001 -p1
%patch20002 -p1
%patch20003 -p1
%patch20004 -p1
%patch20005 -p1
%patch20006 -p1
%patch20007 -p1
%patch20008 -p1
%patch20009 -p1
%patch20010 -p1
%patch20011 -p1
%patch20012 -p1
%patch20013 -p1
%patch20014 -p1
%patch20015 -p1
%patch20016 -p1
%patch20017 -p1
%patch20018 -p1
%patch20019 -p1
%patch20020 -p1
%patch20021 -p1
%patch20022 -p1
%patch20023 -p1
%patch20024 -p1
%patch20025 -p1
%patch20026 -p1
%patch20027 -p1
%patch20028 -p1
%patch20029 -p1
%patch20030 -p1

%patch20031 -p1
%patch20032 -p1
%patch20033 -p1
%patch20034 -p1
%patch20035 -p1

%patch20040 -p1
%patch20041 -p1
%patch20042 -p1
%patch20043 -p1
%patch20044 -p1
%patch20045 -p1
%patch20046 -p1
%patch20047 -p1
%patch20048 -p1
%patch20049 -p1
%patch20050 -p1
%patch20051 -p1
%patch20052 -p1
%patch20053 -p1
%patch20054 -p1
%patch20055 -p1
%build
autoreconf -ivf
export CFLAGS="${RPM_OPT_FLAGS} $CFLAGS"
%configure \
    --enable-xorg \
    --enable-kdrive \
    --enable-kdrive-evdev \
    --enable-kdrive-mouse \
    --enable-xephyr \
    --enable-xnest \
    --disable-xfake \
    --disable-xfbdev \
    --disable-static \
    --without-dtrace \
    --with-pic \
    --with-int10=x86emu \
    --with-default-font-path="/usr/share/fonts/X11/misc" \
    --with-module-dir=%{moduledir} \
    --with-builderstring="Build ID: %{name} %{version}-%{release}" \
    --with-xkb-output=%{_localstatedir}/lib/xkb \
    --enable-record \
    --disable-libunwind \
    --disable-xselinux \
    --disable-config-hal \
    --enable-config-udev \
    --enable-config-udev-kms \
    --disable-install-setuid \
    --enable-suid-wrapper \
    --enable-systemd-logind \
    --with-systemd-daemon \
    --enable-xwayland \
    --enable-glamor \
    --enable-glx \
    --enable-dri2 \
    --enable-dri3 

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT moduledir=%{moduledir}

mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

# Install the vesamodes and extramodes files to let our install/config tools
# be able to parse the same modelist as the X server uses (rhpxl).
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xorg
install -m 0444 hw/xfree86/common/{vesa,extra}modes $RPM_BUILD_ROOT%{_datadir}/xorg/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/xserver

#own this dir.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d 

install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT%{_bindir}/xvfb-run

install -m 755 %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires

# Remove unwanted files/dirs
{
    rm -f $RPM_BUILD_ROOT%{_bindir}/xorgconfig
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xorgconfig.1*
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/Cards
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/Options
    rm -f $RPM_BUILD_ROOT%{_bindir}/in?
    rm -f $RPM_BUILD_ROOT%{_bindir}/ioport
    rm -f $RPM_BUILD_ROOT%{_bindir}/out?
    rm -f $RPM_BUILD_ROOT%{_bindir}/pcitweak
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcitweak.1*
}


%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,root,root,-)
%{_mandir}/man1/Xserver.1*
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

%files Xorg
%defattr(-,root,root,-)
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/X
%{_bindir}/Xorg
%{_libexecdir}/Xorg
%{_bindir}/cvt
%{_bindir}/gtf
%dir %{_datadir}/xorg
%{_datadir}/xorg/vesamodes
%{_datadir}/xorg/extramodes
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libglx.so
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvbe.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libwfb.so
%{_libdir}/xorg/modules/libglamoregl.so
%{_libdir}/xorg/modules/drivers/modesetting_drv.so
%{_mandir}/man1/gtf.1*
%{_mandir}/man1/Xorg.1*
%{_mandir}/man1/cvt.1*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man4/exa.4*
%{_mandir}/man4/modesetting.4*
%{_mandir}/man5/xorg.conf.5*
%{_mandir}/man5/xorg.conf.d.5*
%dir %{_sysconfdir}/X11/xorg.conf.d
%dir %{_datadir}/X11/xorg.conf.d
%{_datadir}/X11/xorg.conf.d/10-quirks.conf 


%if 1
%global Xorgperms %attr(4755, root, root)
%else
# disable until module loading is audited
%global Xorgperms %attr(0711,root,root) %caps(cap_sys_admin,cap_sys_rawio,cap_dac_override=pe)
%endif

%files suid
%defattr(-,root,root,-)
%{Xorgperms} %{_libexecdir}/Xorg.wrap
%{_mandir}/man1/Xorg.wrap.1.gz
%{_mandir}/man5/Xwrapper.config.5.gz

%files Xnest
%defattr(-,root,root,-)
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.1*

%files Xwayland
%defattr(-,root,root,-)
%{_bindir}/Xwayland

%files Xvfb
%defattr(-,root,root,-)
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.1*

%files Xephyr
%defattr(-,root,root,-)
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1.gz

%files devel
%defattr(-,root,root,-)
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{sdkdir}/*.h
%{_datadir}/aclocal/xorg-server.m4

%changelog
* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.18.0-6
- More patches

* Tue Dec 08 2015 Cjacker <cjacker@foxmail.com> - 1.18.0-5
- Backport more patches

* Sun Nov 22 2015 Cjacker <cjacker@foxmail.com> - 1.18.0-4
- Backport some patches from 1.19 git

* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 1.18.0-3
- Fix Xorg.wrap kms detection

* Tue Nov 10 2015 Cjacker <cjacker@foxmail.com> - 1.18.0-2
- Update

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 1.17.4-2
- Update to 1.17.4

* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 1.17.2-18
- Add xvfb-run script

* Fri Oct 23 2015 cjacker - 1.17.2-17
- Rebuild for new 4.0 release

* Mon Jul 13 2015 Cjacker <cjacker@foxmail.com>
- rebuild, enable record extension.
