Summary: EFI Boot Manager
Name: efibootmgr
Version: 14
Release: 1
License: GPLv2+
URL: http://linux.dell.com/%{name}/
BuildRequires: pciutils-devel, zlib-devel
# EFI/UEFI don't exist on PPC
ExclusiveArch: %{ix86} x86_64 ia64

Source0: https://github.com/rhinstaller/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
# efivar.h don't be required 
Patch0: efibootmgr-needless-efivar_h.patch
%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q
%patch0 -p1

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
* Wed Dec 07 2016 sulit - 14-1
- upgrade efibootmgr to 14

* Fri Oct 23 2015 cjacker - 0.5.4-2
- Rebuild for new 4.0 release

