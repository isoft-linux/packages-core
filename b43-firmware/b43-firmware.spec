Name: b43-firmware
Version: 5.100.138
Release: 2
Summary: Broadcom wireless firmware

License: Commercial
URL:  http://www.lwfinger.com/b43-firmware
Source0: http://www.lwfinger.com/b43-firmware/broadcom-wl-5.100.138.tar.bz2
Source1: http://downloads.openwrt.org/sources/wl_apsta-3.130.20.0.o

BuildRequires: b43-fwcutter
BuildArch: noarch

%description
Broadcom wireless firmware

%prep
%setup -c 

%build

%install
mkdir -p %{buildroot}/lib/firmware
b43-fwcutter -w "%{buildroot}/lib/firmware" broadcom-wl-5.100.138/linux/wl_apsta.o
b43-fwcutter -w "%{buildroot}/lib/firmware" %{SOURCE1}
chmod 755 %{buildroot}/lib/firmware/b43
chmod 755 %{buildroot}/lib/firmware/b43legacy

%files
/lib/firmware/b43/
/lib/firmware/b43legacy/

%changelog
* Fri Oct 23 2015 cjacker - 5.100.138-2
- Rebuild for new 4.0 release


