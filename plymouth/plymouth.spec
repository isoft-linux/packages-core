%define plymouthdaemon_execdir %{_sbindir}
%define plymouthclient_execdir %{_bindir}
%define plymouth_libdir %{_libdir}
%define plymouth_initrd_file /boot/initrd-plymouth.img

Summary: Graphical Boot Animation and Logger
Name: plymouth
Version: 0.8.9
Release: 5
License: GPLv2+
Source0: http://freedesktop.org/software/plymouth/releases/%{name}-%{version}.tar.bz2

#for mkinitcpio
Source1: plymouth_install
Source2: plymouth-encrypt_install  
Source3: plymouth_hook             
Source4: plymouth-encrypt_hook     
Source5: isoft-splash.txz

Patch0: dont-timeout-waiting.patch
Patch1: sysfs-tty-fix.patch

URL: http://www.freedesktop.org/wiki/Software/Plymouth

Conflicts: filesystem < 3
Conflicts: systemd < 185-3

BuildRequires: pkgconfig(libdrm)
BuildRequires: kernel-headers
BuildRequires: libpng-devel
BuildRequires: systemd-devel
#for post scripts
Requires(pre): coreutils

%description
Plymouth provides an attractive graphical boot animation in
place of the text messages that normally get shown.  Text
messages are instead redirected to a log file for viewing
after boot.

%package devel
Summary: Libraries and headers for writing Plymouth splash plugins
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the libply and libplybootsplash libraries
and headers needed to develop 3rd party splash plugins for Plymouth.

%prep
%setup -q
%patch0 -p1 -b .dont-timeout-waiting
%patch1 -p1 -b .sysfs-tty-fix

# Change the default theme
#sed -i -e 's/fade-in/spinner/g' src/plymouthd.defaults
sed -i -e 's/fade-in/isoft-splash/g' src/plymouthd.defaults

%build
%configure --enable-tracing --disable-tests \
           --with-logo=%{_datadir}/icons/crystalsvg/128x128/apps/kmenu.png \
           --with-background-start-color-stop=0x0073B3           \
           --with-background-end-color-stop=0x00457E             \
           --with-background-color=0x3391cd                      \
           --disable-gdm-transition                              \
           --enable-systemd-integration                          \
           --without-system-root-install                         \
           --with-rhgb-compat-link                               \
           --disable-gtk    \
           --disable-pango    \
           --without-log-viewer					 \
           --disable-libkms

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


#for mkinitcpio
install -D -m644 %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/initcpio/install/plymouth
install -D -m644 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/initcpio/install/plymouth-encrypt
install -D -m644 %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/initcpio/hooks/plymouth
install -D -m644 %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/initcpio/hooks/plymouth-encrypt



# Glow isn't quite ready for primetime
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/glow/
rm -f $RPM_BUILD_ROOT%{_libdir}/plymouth/glow.so
rm -rf $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/glow

find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} \;

cd $RPM_BUILD_ROOT
tar xf %{SOURCE5} -C usr/share/plymouth/themes/

%clean
rm -rf $RPM_BUILD_ROOT

%post
#plymouth-set-default-theme spinner ||:
plymouth-set-default-theme isoft-splash ||:

%postun
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/plymouth/default.so
    rm -f /boot/initrd-plymouth.img
fi

%files
%defattr(-, root, root)
%dir %{_datadir}/plymouth
%dir %{_datadir}/plymouth/themes
%dir %{_datadir}/plymouth/themes/details
%dir %{_datadir}/plymouth/themes/text
%dir %{_libexecdir}/plymouth
%dir %{_localstatedir}/lib/plymouth
%dir %{_libdir}/plymouth/renderers
%dir %{_sysconfdir}/plymouth
%config(noreplace) %{_sysconfdir}/plymouth/plymouthd.conf
%{plymouthdaemon_execdir}/plymouthd
%{plymouthclient_execdir}/plymouth
%{_bindir}/plymouth
%{_bindir}/rhgb-client
%{_libdir}/plymouth/details.so
%{_libdir}/plymouth/text.so
%{_libdir}/plymouth/renderers/drm*
%{_libdir}/plymouth/renderers/frame-buffer*
%{_datadir}/plymouth/themes/details/details.plymouth
%{_datadir}/plymouth/themes/text/text.plymouth
%{_datadir}/plymouth/plymouthd.defaults
%{_localstatedir}/run/plymouth
%{_localstatedir}/spool/plymouth
%{_mandir}/man?/*
%{_libdir}/systemd/system/*

%{plymouth_libdir}/libply.so.*
%{plymouth_libdir}/libply-splash-core.so.*
%{_libdir}/libply-boot-client.so.*
%dir %{_libdir}/plymouth

%{_libdir}/libply-splash-graphics.so.*

%{_sbindir}/plymouth-set-default-theme
%{_libexecdir}/plymouth/plymouth-update-initrd
%{_libexecdir}/plymouth/plymouth-generate-initrd
%{_libexecdir}/plymouth/plymouth-populate-initrd


#####%{_libdir}/plymouth/label.so

%{_libdir}/plymouth/fade-throbber.so

%dir %{_datadir}/plymouth/themes/fade-in
%{_datadir}/plymouth/themes/fade-in/bullet.png
%{_datadir}/plymouth/themes/fade-in/entry.png
%{_datadir}/plymouth/themes/fade-in/lock.png
%{_datadir}/plymouth/themes/fade-in/star.png
%{_datadir}/plymouth/themes/fade-in/fade-in.plymouth

%dir %{_datadir}/plymouth/themes/isoft-splash
%{_datadir}/plymouth/themes/isoft-splash/background.png
%{_datadir}/plymouth/themes/isoft-splash/logo.png
%{_datadir}/plymouth/themes/isoft-splash/spec0.png
%{_datadir}/plymouth/themes/isoft-splash/spec1.png
%{_datadir}/plymouth/themes/isoft-splash/password_field.png
%{_datadir}/plymouth/themes/isoft-splash/progress_bar.png
%{_datadir}/plymouth/themes/isoft-splash/progress_dot_off.png
%{_datadir}/plymouth/themes/isoft-splash/progress_dot_on.png
%{_datadir}/plymouth/themes/isoft-splash/isoft-splash.plymouth
%{_datadir}/plymouth/themes/isoft-splash/isoft-splash.script

%dir %{_datadir}/plymouth/themes/spinner
%{_datadir}/plymouth/themes/spinner/*.png
%{_datadir}/plymouth/themes/spinner/spinner.plymouth

%{_libdir}/plymouth/throbgress.so

%dir %{_datadir}/plymouth/themes/spinfinity
%{_datadir}/plymouth/themes/spinfinity/box.png
%{_datadir}/plymouth/themes/spinfinity/bullet.png
%{_datadir}/plymouth/themes/spinfinity/entry.png
%{_datadir}/plymouth/themes/spinfinity/lock.png
%{_datadir}/plymouth/themes/spinfinity/throbber-[0-3][0-9].png
%{_datadir}/plymouth/themes/spinfinity/spinfinity.plymouth

%{_libdir}/plymouth/space-flares.so

%dir %{_datadir}/plymouth/themes/solar
%{_datadir}/plymouth/themes/solar/*.png
%{_datadir}/plymouth/themes/solar/solar.plymouth

%{_libdir}/plymouth/two-step.so

%{_libdir}/plymouth/script.so

%dir %{_datadir}/plymouth/themes/script
%{_datadir}/plymouth/themes/script/*.png
%{_datadir}/plymouth/themes/script/script.script
%{_datadir}/plymouth/themes/script/script.plymouth

%{_libdir}/initcpio/install/plymouth*
%{_libdir}/initcpio/hooks/plymouth*


%files devel
%defattr(-, root, root)
%{plymouth_libdir}/libply.so
%{plymouth_libdir}/libply-splash-core.so
%{_libdir}/libply-boot-client.so
%{_libdir}/libply-splash-graphics.so
%{_libdir}/pkgconfig/ply-splash-core.pc
%{_libdir}/pkgconfig/ply-splash-graphics.pc
%{_libdir}/pkgconfig/ply-boot-client.pc
#%{_libdir}/plymouth/renderers/x11*
%{_includedir}/plymouth-1


%changelog
* Mon Nov 02 2015 sulit <sulitsrc@gmail.com> - 0.8.9-5
- redo isoft-splash.txz

* Wed Oct 28 2015 sulit <sulitsrc@gmail.com> - 0.8.9-4
- add isoft-splash

* Fri Oct 23 2015 cjacker - 0.8.9-2
- Rebuild for new 4.0 release

