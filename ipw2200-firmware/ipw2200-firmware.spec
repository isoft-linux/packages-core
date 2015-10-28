Summary: Firmware for Intel® PRO/Wireless 2200 network adaptors
Name: ipw2200-firmware
Version: 3.1
Release: 12%{?dist}
License: Redistributable, no modification permitted
URL: http://ipw2200.sourceforge.net/firmware.php
# License agreement must be displayed before download (referer protection)
Source0: ipw2200-fw-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
# This is so that the noarch packages only appears for these archs
ExclusiveArch: noarch i386 x86_64

%description
This package contains the firmware files required by the ipw2200 driver for
Linux. Usage of the firmware is subject to the terms and conditions contained
in /lib/firmware/LICENSE.ipw2200. Please read it carefully.


%prep
%setup -q -n ipw2200-fw-%{version}


%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/lib/firmware
# Terms state that the LICENSE *must* be in the same directory as the firmware
%{__install} -p -m 0644 *.fw %{buildroot}/lib/firmware/
%{__install} -p -m 0644 LICENSE.ipw2200-fw %{buildroot}/lib/firmware/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc /lib/firmware/LICENSE.ipw2200-fw
/lib/firmware/*.fw


%changelog
* Fri Oct 23 2015 cjacker - 3.1-12
- Rebuild for new 4.0 release

