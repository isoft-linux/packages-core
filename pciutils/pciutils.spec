Name:		pciutils
Version:	3.3.1
Release:    1	
Source:		https://www.kernel.org/pub/software/utils/pciutils/%{name}-%{version}.tar.xz

#change pci.ids directory to hwdata
Patch1:		pciutils-2.2.1-idpath.patch

#add support for directory with another pci.ids, rejected by upstream, rhbz#195327
Patch2:		pciutils-dir-d.patch

License:	GPLv2+
URL:		http://atrey.karlin.mff.cuni.cz/~mj/pciutils.shtml
ExclusiveOS:	Linux
Requires:	hwdata
BuildRequires:	sed
Summary: PCI bus related utilities
Group:  Core/Runtime/Utility 

%description
The pciutils package contains various utilities for inspecting and
setting devices connected to the PCI bus. The utilities provided
require kernel version 2.1.82 or newer (which support the
/proc/bus/pci interface).

%package devel
Summary: Linux PCI development library
Group: Core/Development/Library
Requires: zlib-devel pkgconfig %{name} = %{version}-%{release}

%description devel
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%package libs
Summary: Linux PCI library
Group:  Core/Runtime/Library 

%description libs
This package contains a library for inspecting and setting
devices connected to the PCI bus.

%package devel-static
Summary: Linux PCI static library
Group: Core/Development/Library
Requires: %{name}-devel = %{version}-%{release}

%description devel-static
This package contains a static library for inspecting and setting
devices connected to the PCI bus.

%prep
%setup -q -n pciutils-%{version}
%patch1 -p1 -b .idpath
%patch2 -p1 -b .dird
sed -i -e 's|^SRC=.*|SRC="http://pciids.sourceforge.net/pci.ids"|' update-pciids.sh

%build
make SHARED="no" ZLIB="no" STRIP="" OPT="$RPM_OPT_FLAGS" PREFIX="/usr" IDSDIR="/usr/share/hwdata" PCI_IDS="pci.ids" %{?_smp_mflags}
mv lib/libpci.a lib/libpci.a.toinstall

make clean

make SHARED="yes" ZLIB="no" STRIP="" OPT="$RPM_OPT_FLAGS" PREFIX="/usr" LIBDIR="/%{_lib}" IDSDIR="/usr/share/hwdata" PCI_IDS="pci.ids" %{?_smp_mflags}

#fix lib vs. lib64 in libpci.pc (static Makefile is used)
sed -i "s|^libdir=.*$|libdir=/%{_lib}|" lib/libpci.pc


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{sbin,%{_sbindir},%{_lib},%{_mandir}/man8,%{_libdir},%{_libdir}/pkgconfig,%{_includedir}/pci}

install -p lspci setpci $RPM_BUILD_ROOT/sbin
install -p update-pciids $RPM_BUILD_ROOT/%{_sbindir}
install -p -m 644 lspci.8 setpci.8 update-pciids.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -p lib/libpci.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s ../../%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/*.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpci.so

mv lib/libpci.a.toinstall lib/libpci.a
install -p -m 644 lib/libpci.a $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -N $RPM_BUILD_ROOT/%{_lib}
install -p lib/pci.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p lib/header.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p lib/config.h $RPM_BUILD_ROOT%{_includedir}/pci/config.h
install -p lib/types.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p lib/libpci.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README ChangeLog pciutils.lsm COPYING
/sbin/lspci
/sbin/setpci
%{_sbindir}/update-pciids
%{_mandir}/man8/*

%files libs
%doc COPYING
%defattr(-,root,root,-)
/%{_lib}/libpci.so.*

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/libpci.a

%files devel
%defattr(0644, root, root, 0755)
%{_libdir}/pkgconfig/libpci.pc
%{_libdir}/libpci.so
%{_includedir}/pci

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS
