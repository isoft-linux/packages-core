%global firmware_release 54

%global _firmwarepath	/usr/lib/firmware

Name:		linux-firmware
Version:	20150713
Release:	%{firmware_release}.git%{?dist}
Summary:	Firmware files used by the Linux kernel

Group:		System Environment/Kernel
License:	GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
URL:		http://www.kernel.org/
#git://git.kernel.org/pub/scm/linux/kernel/git/iwlwifi/linux-firmware.git
Source0:	%{name}-%{version}.tar.gz

#according to kernel commit 46c266ff8435422631402284e2a3b62ef1560141
#this two firmware need to be included to support 13d3:3474 AR3012 device
Source1: AthrBT_0x11020100.dfu 
Source2: ramps_0x11020100_40.dfu


BuildArch:	noarch
Provides:	kernel-firmware = %{version} xorg-x11-drv-ati-firmware = 7.0
Conflicts:	microcode_ctl < 2.1-0

BuildRequires: git

%description
This package includes firmware files required for some devices to
operate.

%prep
%setup -q -n linux-firmware
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
mkdir -p $RPM_BUILD_ROOT/%{_firmwarepath}
mkdir -p $RPM_BUILD_ROOT/%{_firmwarepath}/updates
cp -r * $RPM_BUILD_ROOT/%{_firmwarepath}
rm $RPM_BUILD_ROOT/%{_firmwarepath}/{WHENCE,LICENCE.*,LICENSE.*}


install -m 0644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_firmwarepath}/ar3k/

# Create file list but exclude firmwares that we place in subpackages
FILEDIR=`pwd`
pushd $RPM_BUILD_ROOT/%{_firmwarepath}
find . \! -type d > $FILEDIR/linux-firmware.files
find . -type d | sed -e '/^.$/d' > $FILEDIR/linux-firmware.dirs
popd
sed -i -e 's!^!/usr/lib/firmware/!' linux-firmware.{files,dirs}
sed -e 's/^/%%dir /' linux-firmware.dirs >> linux-firmware.files




%clean
rm -rf $RPM_BUILD_ROOT

%files -f linux-firmware.files
%defattr(-,root,root,-)
%dir %{_firmwarepath}
%doc WHENCE LICENCE.* LICENSE.*

%changelog
* Mon Jul 13 2015 Cjacker <cjacker@foxmail.com>
- update, for iwlwifi 13/14/15 firmware

* Tue Jul 07 2015 Cjacker <cjacker@foxmail.com>
- add 13d3:3474 AR3012 device firmware.


