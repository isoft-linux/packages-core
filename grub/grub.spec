# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%global efiarchs %{ix86} x86_64 ia64

%ifarch %{ix86}
%global grubefiarch i386-efi
%global grubefiname grubia32.efi
%global grubeficdname gcdia32.efi
%endif
%ifarch x86_64
%global grubefiarch %{_arch}-efi
%global grubefiname grubx64.efi
%global grubeficdname gcdx64.efi
%endif

%global efidir pure64 

%undefine _missing_build_ids_terminate_build

Name:           grub
Epoch:          1
Version:        2.02
Release:        31 
Summary:        Bootloader with support for Linux, Multiboot and more
Group:          Core/Runtime/Utility
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{version}.tar.xz
Source1:        http://ftp.gnu.org/gnu/unifont/unifont-6.3.20140214/unifont-6.3.20140214.pcf.gz

Source10:       grub-default-config

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel
BuildRequires:  freetype-devel
BuildRequires:  /usr/lib/crt1.o glibc
BuildRequires:	gettext-devel
Requires:	    gettext os-prober which file
Requires:	    %{name}-tools = %{epoch}:%{version}-%{release}

%description
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for PC BIOS systems.

%ifarch %{efiarchs}
%package efi
Summary:	GRUB for EFI systems.
Group:		Core/Runtime/Utility
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.
%endif

%package tools
Summary:	Support tools for GRUB.
Group:		Core/Runtime/Utility
Requires:	gettext os-prober which file

%description tools
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides tools for support of all platforms.

%prep
%setup -q -c -n grub-%{version} -a 0
cd grub-%{version}
autoreconf -ivf
# place unifont in the '.' from which configure is run
cp %{SOURCE1} unifont.pcf.gz
sed 's|GNU/Linux|Linux|' -i util/grub.d/10_linux.in
cd ..

%ifarch %{efiarchs}
cp -r grub-%{version} grub-efi-%{version}
%endif

%build
%ifarch %{efiarchs}
cd grub-efi-%{version}
./configure --prefix=/usr \
    --exec-prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/sbin \
    --sysconfdir=/etc \
    --datadir=/usr/share \
    --includedir=/usr/include \
    --libdir=/usr/lib \
    --libexecdir=/usr/libexec \
    --localstatedir=/var \
    --sharedstatedir=/var/lib \
    --mandir=/usr/share/man \
    --infodir=/usr/share/info \
    TARGET_LDFLAGS=-static \
    --with-platform=efi \
    --with-bootdir="/boot" \
    --with-grubdir="grub" \
    --disable-grub-mount \
    --disable-werror
make %{?_smp_mflags}
GRUB_MODULES="all_video boot btrfs cat chain configfile echo \
		efinet ext2 fat font gfxmenu gfxterm gzio halt hfsplus iso9660 \
		jpeg lvm minicmd normal part_msdos \
		part_gpt password_pbkdf2 png reboot search search_fs_uuid \
		search_fs_file search_label sleep test video xfs \
		mdraid09 mdraid1x linux multiboot2 multiboot"
./grub-mkimage -O %{grubefiarch} -o %{grubeficdname} -p /EFI/BOOT \
		-d grub-core ${GRUB_MODULES}
./grub-mkimage -O %{grubefiarch} -o %{grubefiname} -p /EFI/%{efidir} \
		-d grub-core ${GRUB_MODULES}
cd ..
%endif

cd grub-%{version}
./configure --prefix=/usr \
    --exec-prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/sbin \
    --sysconfdir=/etc \
    --datadir=/usr/share \
    --includedir=/usr/include \
    --libdir=/usr/lib \
    --libexecdir=/usr/libexec \
    --localstatedir=/var \
    --sharedstatedir=/var/lib \
    --mandir=/usr/share/man \
    --infodir=/usr/share/info \
    TARGET_LDFLAGS=-static \
    --with-platform=pc \
    --with-bootdir="/boot" \
    --with-grubdir="grub" \
    --disable-grub-mount \
    --disable-werror

make %{?_smp_mflags}

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efiarchs}
cd grub-efi-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -iname "*.module" -exec chmod a-x {} \;
install -D -m 755 %{grubefiname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubefiname}
install -D -m 755 %{grubeficdname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubeficdname}
install -D -m 644 unicode.pf2 $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/fonts/unicode.pf2
cd ..
%endif

cd grub-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg

rm -rf $RPM_BUILD_ROOT%{_infodir}

# Defaults
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/default
install -m0644 %{SOURCE10} ${RPM_BUILD_ROOT}%{_sysconfdir}/default/grub
cd ..

%clean    
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/grub/*-pc/
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{version}/COPYING

%ifarch %{efiarchs}
%files efi
%defattr(-,root,root,-)
%{_libdir}/grub/%{grubefiarch}
%attr(0755,root,root)/boot/efi/EFI/%{efidir}
%doc grub-%{version}/COPYING
%endif

%files tools 
%defattr(-,root,root,-)
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%{_datarootdir}/grub/*
%{_sbindir}/*
%{_bindir}/*
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/bash_completion.d/grub
%dir /boot/%{name}
%exclude %{_mandir}
%doc grub-%{version}/COPYING grub-%{version}/INSTALL
%doc grub-%{version}/NEWS grub-%{version}/README
%doc grub-%{version}/THANKS grub-%{version}/TODO
%doc grub-%{version}/ChangeLog
%doc grub-%{version}/grub-dev.html grub-%{version}/docs/font_char_metrics.png

%changelog
