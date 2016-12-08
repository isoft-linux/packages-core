%define efivar_ver 30
Summary: EFI Boot Manager
Name: efibootmgr
Version: 14
Release: 1
License: GPLv2+
URL: http://linux.dell.com/%{name}/
BuildRequires: pciutils-devel, zlib-devel
BuildRequires: efivar-libs >= 30-1, efivar-devel >= 30-1
BuildRequires: popt-devel popt-static
# EFI/UEFI don't exist on PPC
ExclusiveArch: %{ix86} x86_64 ia64

Source0: https://github.com/rhinstaller/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q

%build
make %{?_smp_mflags} EXTRA_CFLAGS='%{optflags}'

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_sbindir}/efibootdump
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/efibootdump.8.gz
%doc README INSTALL COPYING
    
%changelog
* Wed Dec 07 2016 sulit - 14-1
- upgrade efibootmgr to 14
- add BuildRequires popt-devel and popt-static

* Fri Oct 23 2015 cjacker - 0.5.4-2
- Rebuild for new 4.0 release

