Name:		rtl8192u-firmware
Summary:	Firmware files for Realtek RTL8192 USB WLAN adapters
Version:	1.0
Release:	1.1
License:	Any Proprietary
Url:		ftp://ftp.dlink.com/Wireless/dwa130_revC/Drivers/dwa130_revC_drivers_linux_006.zip
Source0:	%{name}.tar.bz2
Source2:	LICENCE
BuildArch:	noarch

%description
This package contains binary firmware images for Realtek RTL8192 USB WLAN adapters.
 
The firmware files will be copied to /lib/firmware/RTL8192U, they were obtained from version 
2.6.0006.1031.2008 of the vendor driver which could be found here:

ftp://ftp.dlink.com/Wireless/dwa130_revC/Drivers/dwa130_revC_drivers_linux_006.zip

%prep
# nothing to do

%build
# nothing to do

%install
install -d $RPM_BUILD_ROOT/lib/firmware
tar -xf %{SOURCE0} -C $RPM_BUILD_ROOT/lib/firmware/
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/lib/firmware/RTL8192U/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /lib/firmware/RTL8192U
/lib/firmware/RTL8192U/*

%changelog
* Mon Aug 23 2015 Cjacker <cjacker@foxmail.com>
- initial package
