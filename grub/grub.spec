%define debug_package %{nil}

# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif
# sparc is always compiled 64 bit
%ifarch %{sparc}
%define _target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if ! 0%{?efi}

%global efi_only aarch64
%global efiarchs %{ix86} x86_64 ia64 %{efi_only}

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
%ifarch aarch64
%global grubefiarch arm64-efi
%global grubefiname grubaa64.efi
%global grubeficdname gcdaa64.efi
%endif

# Figure out the right file path to use
%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//'))

%endif

%global tarversion 2.02~beta2
%undefine _missing_build_ids_terminate_build

Name:           grub
Epoch:          1
Version:        2.02
Release:        33%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source3: 	dejavu-fonts-ttf-2.35.tar.bz2
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore

# generate with:
# git diff grub-2.02-beta2..origin/master
Patch0000: grub-2.02-beta2-to-origin-master.patch

Patch0001: 0001-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0002: 0002-Add-fw_path-variable-revised.patch
Patch0003: 0003-Add-support-for-linuxefi.patch
Patch0004: 0004-Use-linuxefi-and-initrdefi-where-appropriate.patch
Patch0005: 0005-Don-t-allow-insmod-when-secure-boot-is-enabled.patch
Patch0006: 0006-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0007: 0007-Fix-crash-on-http.patch
Patch0008: 0008-IBM-client-architecture-CAS-reboot-support.patch
Patch0009: 0009-Add-vlan-tag-support.patch
Patch0010: 0010-Add-X-option-to-printf-functions.patch
Patch0011: 0011-DHCP-client-ID-and-UUID-options-added.patch
Patch0012: 0012-Search-for-specific-config-file-for-netboot.patch
Patch0013: 0013-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0014: 0014-Move-bash-completion-script-922997.patch
Patch0015: 0015-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0016: 0016-Don-t-write-messages-to-the-screen.patch
Patch0017: 0017-Don-t-print-GNU-GRUB-header.patch
Patch0018: 0018-Don-t-add-to-highlighted-row.patch
Patch0019: 0019-Message-string-cleanups.patch
Patch0020: 0020-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0021: 0021-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0022: 0022-Indent-menu-entries.patch
Patch0023: 0023-Fix-margins.patch
Patch0024: 0024-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0025: 0025-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0026: 0026-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0027: 0027-Use-linux16-when-appropriate-880840.patch
Patch0028: 0028-Enable-pager-by-default.-985860.patch
Patch0029: 0029-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0030: 0030-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0031: 0031-Don-t-draw-a-border-around-the-menu.patch
Patch0032: 0032-Use-the-standard-margin-for-the-timeout-string.patch
Patch0033: 0033-Fix-grub_script_execute_sourcecode-usage-on-ppc.patch
Patch0034: 0034-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0035: 0035-Make-10_linux-work-with-our-changes-for-linux16-and-.patch
Patch0036: 0036-Don-t-print-during-fdt-loading-method.patch
Patch0037: 0037-Honor-a-symlink-when-generating-configuration-by-gru.patch
Patch0038: 0038-Don-t-munge-raw-spaces-when-we-re-doing-our-cmdline-.patch
Patch0039: 0039-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0040: 0040-Don-t-emit-Booting-.-message.patch
Patch0041: 0041-Make-CTRL-and-ALT-keys-work-as-expected-on-EFI-syste.patch
Patch0042: 0042-May-as-well-try-it.patch
Patch0043: 0043-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0044: 0044-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0045: 0045-trim-arp-packets-with-abnormal-size.patch
Patch0046: 0046-Fix-convert-function-to-support-NVMe-devices.patch
Patch0047: 0047-Fix-bad-test-on-GRUB_DISABLE_SUBMENU.patch
Patch0048: 0048-Switch-to-use-APM-Mustang-device-tree-for-hardware-t.patch
Patch0049: 0049-Use-the-default-device-tree-from-the-grub-default-fi.patch
Patch0050: 0050-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
Patch0051: 0051-Reduce-timer-event-frequency-by-10.patch
Patch0052: 0052-always-return-error-to-UEFI.patch
Patch0053: 0053-Suport-for-bi-endianess-in-elf-file.patch
Patch0054: 0054-Add-grub_util_readlink.patch
Patch0055: 0055-Make-editenv-chase-symlinks-including-those-across-d.patch
Patch0056: 0056-Generate-OS-and-CLASS-in-10_linux-from-etc-os-releas.patch
Patch0057: 0057-Fix-GRUB_DISABLE_SUBMENU-one-more-time.patch
Patch0058: 0058-Minimize-the-sort-ordering-for-.debug-and-rescue-ker.patch
Patch0059: 0059-Add-GRUB_DISABLE_UUID.patch
Patch0060: 0060-Allow-fallback-to-include-entries-by-title-not-just-.patch
Patch0061: 0061-Load-arm-with-SB-enabled.patch
Patch0062: 0062-Try-prefix-if-fw_path-doesn-t-work.patch
Patch0063: 0063-Try-to-emit-linux16-initrd16-and-linuxefi-initrdefi-.patch
Patch0064: 0064-Update-to-minilzo-2.08.patch
Patch0065: 0065-Make-grub2-mkconfig-construct-titles-that-look-like-.patch
Patch0066: 0066-Make-rescue-and-debug-entries-sort-right-again-in-gr.patch
Patch0067: 0067-Make-.gitignore-suck-way-less.patch
Patch0068: 0068-Update-info-with-grub.cfg-netboot-selection-order-11.patch
Patch0069: 0069-Use-Distribution-Package-Sort-for-grub2-mkconfig-112.patch
Patch0070: 0070-Add-friendly-grub2-password-config-tool-985962.patch
Patch0071: 0071-Make-exit-take-a-return-code.patch
Patch0072: 0072-Add-some-__unused__-where-gcc-5.x-is-more-picky-abou.patch
Patch0073: 0073-Fix-race-in-EFI-validation.patch
Patch0074: 0074-Mark-po-exclude.pot-as-binary-so-git-won-t-try-to-di.patch




Patch10001: 10001-Put-the-correct-.file-directives-in-our-.S-files.patch
Patch10002: 10002-Make-efi-machines-load-an-env-block-from-a-variable.patch
Patch10003: 10003-Make-it-possible-to-enabled-build-id-sha1.patch
#Patch10004: 10004-Don-t-tell-the-compiler-to-do-annoying-things-with-f.patch
Patch10005: 10005-Add-grub_qdprintf-grub_dprintf-without-the-file-line.patch
Patch10006: 10006-Make-a-gdb-dprintf-that-tells-us-load-addresses.patch

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel bzip2-devel
BuildRequires:  freetype-devel libusb-devel
BuildRequires:	librpm-devel
%ifarch %{sparc} x86_64 aarch64 ppc64le
# sparc builds need 64 bit glibc-devel - also for 32 bit userland
BuildRequires:  /usr/lib64/crt1.o glibc-static
%else
# ppc64 builds need the ppc crt1.o
BuildRequires:  /usr/lib/crt1.o glibc-static
%endif
BuildRequires:  autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git
BuildRequires:	texinfo
BuildRequires:	help2man

Requires:	gettext which file
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Requires:	os-prober >= 1.58-11
Requires(pre):  dracut
Requires(post): dracut

ExcludeArch:	s390 s390x %{arm}

%description
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for PC BIOS systems.

%ifarch %{efiarchs}
%package efi
Summary:	GRUB for EFI systems.
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.

%package efi-modules
Summary:	Modules used to build custom grub.efi images
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}

%description efi-modules
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for rebuilding your own grub.efi on EFI systems.
%endif

%package tools
Summary:	Support tools for GRUB.
Requires:	gettext os-prober which file 
#Requires: system-logos

%description tools
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides tools for support of all platforms.

%package starfield-theme
Summary:	An example theme for GRUB.
#Requires:	system-logos

%description starfield-theme
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides an example theme for the grub screen.

%prep
%setup -T -c -n grub-%{tarversion}
%ifarch %{efiarchs}
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
#put dejavu ttf font here.
tar jxf %{SOURCE3} -C .
rm -rf *.ttf
cp dejavu-fonts-ttf-2.35/ttf/*.ttf .

# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "cjacker@foxmail.com"
git config user.name "Cjacker"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
cd ..
mv grub-%{tarversion} grub-efi-%{tarversion}
%endif

%ifarch %{efi_only}
ln -s grub-efi-%{tarversion} grub-%{tarversion}
%else
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
#put dejavu ttf font here.
tar jxf %{SOURCE3} -C .
rm -rf *.ttf
cp dejavu-fonts-ttf-2.35/ttf/*.ttf .

# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "cjacker@foxmail.com"
git config user.name "Cjacker"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
%endif

%build
%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
./autogen.sh
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=efi					\
	--with-grubdir=%{name}					\
	--disable-grub-mount					\
	--disable-werror
make %{?_smp_mflags}

GRUB_MODULES="	all_video boot btrfs cat chain configfile echo \
		efifwsetup efinet ext2 fat font gfxmenu gfxterm gzio halt \
		hfsplus iso9660 jpeg loadenv loopback lvm mdraid09 mdraid1x \
		minicmd normal part_apple part_msdos part_gpt \
		password_pbkdf2 png \
		reboot search search_fs_uuid search_fs_file search_label \
		serial sleep syslinuxcfg test tftp video xfs"
%ifarch aarch64
GRUB_MODULES+=" linux "
%else
GRUB_MODULES+=" backtrace usb usbserial_common "
GRUB_MODULES+=" usbserial_pl2303 usbserial_ftdi usbserial_usbdebug "
GRUB_MODULES+=" linuxefi multiboot2 multiboot "
%endif
./grub-mkimage -O %{grubefiarch} -o %{grubefiname}.orig -p /EFI/%{efidir} \
		-d grub-core ${GRUB_MODULES}
./grub-mkimage -O %{grubefiarch} -o %{grubeficdname}.orig -p /EFI/BOOT \
		-d grub-core ${GRUB_MODULES}
mv %{grubefiname}.orig %{grubefiname}
mv %{grubeficdname}.orig %{grubeficdname}



cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
./autogen.sh
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%ifarch %{sparc} ppc ppc64 ppc64le
%define platform ieee1275
%else
%define platform pc
%endif
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-m64//g'					\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/-mcpu=power7/-mcpu=power6/g'		\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=%{platform}				\
	--with-grubdir=%{name}					\
	--enable-grub-themes					\
	--disable-grub-mount					\
	--disable-werror

make %{?_smp_mflags}
%endif

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -iname "*.module" -exec chmod a-x {} \;

# Ghost config file
install -m 755 -d $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/
touch $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/grub.cfg
ln -s ../boot/efi/EFI/%{efidir}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-efi.cfg

install -m 755 %{grubefiname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubefiname}
install -m 755 %{grubeficdname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubeficdname}
install -D -m 644 unicode.pf2 $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/fonts/unicode.pf2
cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
make DESTDIR=$RPM_BUILD_ROOT install

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
%endif

cp -a $RPM_BUILD_ROOT%{_datarootdir}/locale/en\@quot $RPM_BUILD_ROOT%{_datarootdir}/locale/en

#we do not ship infos.
rm -rf $RPM_BUILD_ROOT%{_infodir}

# Defaults
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/default
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/default/grub
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub \
	${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/grub

cd ..
%find_lang grub

# iSoft theme in /boot/grub/themes/system/
cd $RPM_BUILD_ROOT
tar xjf %{SOURCE5}
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub/themes/system/DejaVuSans-10.pf2      -s 10 /usr/share/fonts/DejaVuSans.ttf # "DejaVu Sans Regular 10"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub/themes/system/DejaVuSans-12.pf2      -s 12 /usr/share/fonts/DejaVuSans.ttf # "DejaVu Sans Regular 12"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub/themes/system/DejaVuSans-Bold-14.pf2 -s 14 /usr/share/fonts/DejaVuSans-Bold.ttf # "DejaVu Sans Bold 14"

#prelink ignore
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/grub.conf
# these have execstack, and break under selinux
-b /usr/bin/grub-script-check
-b /usr/bin/grub-mkrelpath
-b /usr/bin/grub-fstest
-b /usr/sbin/grub-bios-setup
-b /usr/sbin/grub-probe
-b /usr/sbin/grub-sparc64-setup
EOF

%ifarch %{efiarchs}
mkdir -p boot/efi/EFI/%{efidir}/
ln -s /boot/efi/EFI/%{efidir}/grubenv boot/grub/grubenv
%endif

%clean    
rm -rf $RPM_BUILD_ROOT

%ifnarch %{efi_only}
%files -f grub.lang
%defattr(-,root,root,-)
%{_libdir}/grub/*-%{platform}/
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{tarversion}/COPYING
%config(noreplace) %ghost /boot/grub/grubenv
%endif

%ifarch %{efiarchs}
%files efi
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg
%attr(0755,root,root)/boot/efi/EFI/%{efidir}
%attr(0755,root,root)/boot/efi/EFI/%{efidir}/fonts
%ghost %config(noreplace) /boot/efi/EFI/%{efidir}/grub.cfg
%doc grub-%{tarversion}/COPYING
/boot/grub/grubenv
# I know 0700 seems strange, but it lives on FAT so that's what it'll
# get no matter what we do.
%config(noreplace) %ghost %attr(0700,root,root)/boot/efi/EFI/%{efidir}/grubenv

%files efi-modules
%defattr(-,root,root,-)
%{_libdir}/grub/%{grubefiarch}
%endif

%files tools -f grub.lang
%defattr(-,root,root,-)
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/*
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-rpm-sort
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-setpassword
%{_sbindir}/%{name}-sparc64-setup
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-file
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-syslinux2cfg
%{_datarootdir}/bash-completion/completions/grub
%{_sysconfdir}/prelink.conf.d/grub.conf
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/sysconfig/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes/
%dir /boot/%{name}/themes/system
%exclude /boot/%{name}/themes/system/*
%exclude %{_datarootdir}/grub/themes/
%{_datadir}/man/man?/*
%doc grub-%{tarversion}/COPYING grub-%{tarversion}/INSTALL
%doc grub-%{tarversion}/NEWS grub-%{tarversion}/README
%doc grub-%{tarversion}/THANKS grub-%{tarversion}/TODO
%doc grub-%{tarversion}/themes/starfield/COPYING.CC-BY-SA-3.0

%files starfield-theme
%dir /boot/%{name}/themes/
/boot/%{name}/themes/system
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/themes/starfield

%changelog
* Fri Oct 23 2015 cjacker - 1:2.02-33
- Rebuild for new 4.0 release

