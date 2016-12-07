%define efivar_ver 30
Summary: EFI Boot Manager
Name: efibootmgr
Version: 14
Release: 1
License: GPLv2+
URL: http://linux.dell.com/%{name}/
BuildRequires: pciutils-devel, zlib-devel
BuildRequires: popt-devel popt
Requires: popt
# EFI/UEFI don't exist on PPC
ExclusiveArch: %{ix86} x86_64 ia64

Source0: https://github.com/rhinstaller/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
Source1: https://github.com/rhinstaller/efivar/releases/download/%{efivar_ver}/efivar-%{efivar_ver}.tar.bz2
# efivar.h don't be required 
%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q
tar xf %{SOURCE1} 
sed -i -e \
		's/gcc-ar/ar/g' \
		efivar-%{efivar_ver}/Make.defaults
sed -i -e \
		's/lib64/lib/g' \
		efivar-%{efivar_ver}/Make.defaults
sed -i -e \
		's@-I$(SRCDIR)/include@-I$(SRCDIR)/include -I../efivar-%{efivar_ver}/src/include/efivar -L../efivar-%{efivar_ver}/src@g' \
		src/Makefile

%build
cd %{_builddir}/%{name}-%{version}/efivar-%{efivar_ver}
make %{?_smp_mflags} libdir=%{_libdir} bindir=%{_bindir} CFLAGS="$RPM_OPT_FLAGS -flto" LDFLAGS="$RPM_LD_FLAGS -flto"
cd %{_builddir}/%{name}-%{version}
make %{?_smp_mflags} EXTRA_CFLAGS='%{optflags}'

%install
rm -rf %{buildroot}
cd %{_builddir}/%{name}-%{version}/efivar-%{efivar_ver} && %make_install
cd %{_builddir}/%{name}-%{version} && %make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
#efivar
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/efivar
%exclude %{_bindir}/efivar-static
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so.*
#efibootmgr
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_sbindir}/efibootdump
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/efibootdump.8.gz
%doc README INSTALL COPYING
    
%changelog
* Wed Dec 07 2016 sulit - 14-1
- upgrade efibootmgr to 14
- add efivar to efbootmgr package
- add BuildRequires popt-devel

* Fri Oct 23 2015 cjacker - 0.5.4-2
- Rebuild for new 4.0 release

