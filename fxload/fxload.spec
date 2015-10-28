Name: fxload
Version: 2008_10_13
Release: 4%{?dist}
Summary: A helper program to download firmware into FX and FX2 EZ-USB devices

License: GPLv2+
URL: http://linux-hotplug.sourceforge.net/
Source0: fxload-%{version}-noa3load.tar.gz
# The above file is derived from:
# http://downloads.sourceforge.net/project/linux-hotplug/fxload/2008_10_13/fxload-2008_10_13.tar.gz
# This file contains code that is copyright Cypress Semiconductor Inc,
# and cannot be distributed. Therefore we use this script to remove the
# copyright code before shipping it. Download the upstream tarball and
# invoke this script while in the tarball's directory:
# ./fxload-generate-tarball.sh 2008_10_13
Source1: fxload-generate-tarball.sh
Patch0: fxload-noa3load.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: kernel-headers
Requires: udev
Conflicts: hotplug-gtk hotplug

%description 
This program is conveniently able to download firmware into FX and FX2
EZ-USB devices, as well as the original AnchorChips EZ-USB.  It is
intended to be invoked by udev scripts when the unprogrammed device
appears on the bus.

%prep
%setup -q 
%patch0 -p1 -b .fxload-noa3load

%build 
make

%install
rm -rf %{buildroot}
mkdir -p -m 755 %{buildroot}/sbin
install -m 755 fxload %{buildroot}/sbin
mkdir -p -m 755 %{buildroot}/%{_mandir}/man8/
install -m 644 fxload.8 %{buildroot}/%{_mandir}/man8/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING
%doc README.txt
%attr(0755, root, root) /sbin/fxload
%{_mandir}/*/*

%changelog
* Fri Oct 23 2015 cjacker - 2008_10_13-4
- Rebuild for new 4.0 release

