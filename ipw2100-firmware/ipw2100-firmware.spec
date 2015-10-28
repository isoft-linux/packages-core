Summary: Firmware for Intel® PRO/Wireless 2100 network adaptors
Name: ipw2100-firmware
Version: 1.3
Release: 19%{?dist}
License: Redistributable, no modification permitted
URL: http://ipw2100.sourceforge.net/firmware.php
# License agreement must be displayed before download (referer protection)
Source: ipw2100-fw-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
# This is so that the noarch packages only appears for these archs
ExclusiveArch: noarch i386 x86_64

%description
This package contains the firmware files required by the ipw2100 driver for
Linux. Usage of the firmware is subject to the terms and conditions contained
in /lib/firmware/LICENSE.ipw2100. Please read it carefully.


%prep
%setup -q -c


%build


%install
%{__rm} -rf %{buildroot} _doc/
%{__mkdir_p} %{buildroot}/lib/firmware
# Terms state that the LICENSE *must* be in the same directory as the firmware
%{__install} -p -m 0644 *.fw %{buildroot}/lib/firmware/
%{__install} -p -m 0644 LICENSE %{buildroot}/lib/firmware/LICENSE.ipw2100
# Symlink to include as %%doc
%{__mkdir} _doc
%{__ln_s} /lib/firmware/LICENSE.ipw2100 _doc/LICENSE


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc _doc/*
/lib/firmware/LICENSE.ipw2100
/lib/firmware/*.fw


%changelog
* Fri Oct 23 2015 cjacker - 1.3-19
- Rebuild for new 4.0 release

