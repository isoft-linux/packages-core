%global firmware_release 59

%global _firmwarepath	/lib/firmware

Name: linux-firmware
Version: 20151117
Release: %{firmware_release}.git%{?dist}.5
Summary: Firmware files used by the Linux kernel
License: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL: http://www.kernel.org/
#git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
Source0: linux-firmware-%{version}.tar.xz 

#git repos hold the lastest iwlwifi ucode.
#git://git.kernel.org/pub/scm/linux/kernel/git/iwlwifi/linux-firmware.git
Source1: %{name}-iwlwifi.tar.gz

#A helper utility to scan kernel modules and find missing firmwares need to be supply.
Source2: find-missing-firmware 


#6fire usb sound card.
#http://sourceforge.net/projects/sixfireusb/files/tools/fwinst.sh
Source10: 6fire-fwinst.sh
#firmware extracted by fwinst.sh
Source11: dmx6fireap.ihx
Source12: dmx6firel2.ihx
Source13: dmx6firecf.bin

#orinoco wireless device firmware
#http://sourceforge.net/projects/orinoco
#this is a modified tarball with firmwares pre-generated.
Source20: orinoco-fwutils-0.3.tar.gz

#wget "http://git.shaftnet.org/git/gitweb.cgi?p=linux-wlan-ng.git;a=blob_plain;f=src/prism2/ru010803.hex;hb=HEAD" -O prism2_ru.hex
#srec2fw prism2_ru.hex prism2_ru.fw
Source30: prism2_ru.fw
Source31: srec2fw.c

#pre-generated apple isight firmware.
#https://launchpadlibrarian.net/56940925/isight.fw
Source40: isight.fw

BuildArch:	noarch
Provides:	kernel-firmware = %{version} xorg-x11-drv-ati-firmware = 7.0
Conflicts:	microcode_ctl < 2.1-0

BuildRequires: git

%description
This package includes firmware files required for some devices to
operate.

%prep
%setup -q -n linux-firmware -a1 -a20
#pushd %{name}-iwlwifi
#for i in `find . -type f`; do
#  if [ ! -f "`pwd`/../$i" ]; then
#	cp $i `pwd`/../$i
#  fi
#done
#popd

rm -rf iwlwifi*.ucode
cp %{name}-iwlwifi/iwlwifi*.ucode .
rm -rf %{name}-iwlwifi

%build
# Remove firmware shipped in separate packages already
# Perhaps these should be built as subpackages of linux-firmware?
rm -rf ess korg sb16 yamaha

# Remove source files we don't need to install
rm -f usbdux/*dux */*.asm
rm -rf carl9170fw

# No need to install old firmware versions where we also provide newer versions
# which are preferred and support the same (or more) hardware
rm -f libertas/sd8686_v8*
rm -f libertas/usb8388_v5.bin

# Remove firmware for Creative CA0132 HD as it's in alsa-firmware
rm -f ctefx.bin ctspeq.bin

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_firmwarepath}
mkdir -p $RPM_BUILD_ROOT/%{_firmwarepath}/updates
cp -r * $RPM_BUILD_ROOT/%{_firmwarepath}
rm $RPM_BUILD_ROOT/%{_firmwarepath}/{WHENCE,LICENCE.*,LICENSE.*}

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{_bindir}/

#6fire usb sound card firmware
mkdir -p $RPM_BUILD_ROOT/%{_firmwarepath}/6fire
install -m 0644 %{SOURCE11} %{SOURCE12} %{SOURCE13} $RPM_BUILD_ROOT/%{_firmwarepath}/6fire

#orinoco firmwares
pushd orinoco-fwutils-0.3 
#./get_ezusb_fw
#./get_prism_ap_fw
#./get_symbol_fw
install -m0644 symbol_sp24t_prim_fw $RPM_BUILD_ROOT/%{_firmwarepath}
install -m0644 symbol_sp24t_sec_fw $RPM_BUILD_ROOT/%{_firmwarepath}
install -m0644 orinoco_ezusb_fw $RPM_BUILD_ROOT/%{_firmwarepath}
install -m0644 tf020004.hex $RPM_BUILD_ROOT/%{_firmwarepath}/prism_ap_fw.bin
popd


#prism2_usb firmware
install -m 0644 %{SOURCE30} $RPM_BUILD_ROOT/%{_firmwarepath}

#isight firmware
install -m 0644 %{SOURCE40} $RPM_BUILD_ROOT/%{_firmwarepath}

# Create file list but exclude firmwares that we place in subpackages
FILEDIR=`pwd`
pushd $RPM_BUILD_ROOT/%{_firmwarepath}
find . \! -type d > $FILEDIR/linux-firmware.files
find . -type d | sed -e '/^.$/d' > $FILEDIR/linux-firmware.dirs
popd
sed -i -e 's!^!/lib/firmware/!' linux-firmware.{files,dirs}
sed -e 's/^/%%dir /' linux-firmware.dirs >> linux-firmware.files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f linux-firmware.files
%defattr(-,root,root,-)
%{_bindir}/find-missing-firmware
%dir %{_firmwarepath}
%doc WHENCE LICENCE.* LICENSE.*

%changelog
* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 20151117-59.git.5
- Include some missing firmwares

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 20151117-58.git.4
- Update to 20151117, add amd stoney firmware, prepare for kernel 4.4

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 20151105-58.git.3
- Update, add Intel Skylake audio firmware

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 20151013-58.git.2
- Update to latest git.
- Change firmware path from /usr/lib to /lib.

* Fri Oct 23 2015 cjacker - 20151013-56.git.1
- Rebuild for new 4.0 release

* Tue Oct 13 2015 Cjacker <cjacker@foxmail.com>
- update to latest git

* Fri Sep 25 2015 Cjacker <cjacker@foxmail.com>
- update to latest git for Intel Skylake & Broxton Linux Graphics

* Sun Sep 13 2015 Cjacker <cjacker@foxmail.com>
- update to iwlwifi latest git to support kernel-4.3

* Mon Sep 07 2015 Cjacker <cjacker@foxmail.com>
- update to latest git.
- amdgpu firmware already in main repos.

* Sun Aug 23 2015 Cjacker <cjacker@foxmail.com>
- rebase to main git.
- add iwlwifi firmwares need by kernel 4.2 from iwlwifi firmware git.
- add a simple script to help find missing firmwares.

* Mon Jul 13 2015 Cjacker <cjacker@foxmail.com>
- update, for iwlwifi 13/14/15 firmware

* Tue Jul 07 2015 Cjacker <cjacker@foxmail.com>
- add 13d3:3474 AR3012 device firmware.


