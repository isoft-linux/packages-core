Summary: EFI Boot Manager
Name: efibootmgr
Version: 0.5.4
Release: 1
Group: Core/Runtime/Utility
License: GPLv2+
URL: http://linux.dell.com/%{name}/
BuildRequires: pciutils-devel, zlib-devel
# EFI/UEFI don't exist on PPC
ExclusiveArch: %{ix86} x86_64 ia64

Source0: http://linux.dell.com/%{name}/permalink/%{name}-%{version}.tar.gz
Patch0: efibootmgr-0.5.4-default-to-grub.patch
Patch1: efibootmgr-0.5.4-support-4k-sectors.patch
Patch2: efibootmgr-0.5.4-Work-around-broken-Apple-firmware.patch
Patch3: efibootmgr-0.5.4-Remove-device-path-padding-on-non-Itanium.patch
Patch4: efibootmgr-0.5.4-fix-minor-memory-leak.patch
Patch5: efibootmgr-0.5.4-fix-disk-minor-number-discovery.patch
Patch6: efibootmgr-0.5.4-make_boot_var-does-not-check-for-failed-status-with-.patch
Patch10: efibootmgr-fix-clang-build.patch
%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch10 -p1

%build
make %{?_smp_mflags} EXTRA_CFLAGS='%{optflags}'

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_mandir}/man8
install -p --mode 755 src/%{name}/%{name} %{buildroot}%{_sbindir}
gzip -9 -c src/man/man8/%{name}.8 > src/man/man8/%{name}.8.gz
touch -r src/man/man8/%{name}.8 src/man/man8/%{name}.8.gz
install -p --mode 644 src/man/man8/%{name}.8.gz %{buildroot}%{_mandir}/man8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz
%doc README INSTALL COPYING
    
%changelog
