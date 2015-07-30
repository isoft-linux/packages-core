Name:           os-prober
Version:        1.65
Release:        1 
Summary:        Probes disks on the system for installed operating systems

Group:          Core/Runtime/Utility
# For more information about licensing, see copyright file.
License:        GPLv2+ and GPL+
URL:            http://kitenet.net/~joey/code/os-prober/
Source0:        http://ftp.de.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.xz
# move newns binary outside of os-prober subdirectory, so that debuginfo
# can be automatically generated for it
Patch0:         os-prober-newnsdirfix.patch
Patch1:         os-prober-no-dummy-mach-kernel.patch
# Sent upstream
Patch2:         os-prober-mdraidfix.patch
Patch3:         os-prober-yaboot-parsefix.patch
Patch4:         os-prober-usrmovefix.patch
Patch5:         os-prober-remove-basename.patch
Patch6:         os-prober-disable-debug-test.patch
Patch7:         os-prober-btrfsfix.patch
Patch8:         os-prober-bootpart-name-fix.patch
Patch9:         os-prober-mounted-partitions-fix.patch
Patch10:        os-prober-factor-out-logger.patch
Patch11:        os-prober-add-pure64.patch 
Requires:       udev coreutils util-linux
Requires:       grep /bin/sed /sbin/modprobe

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%setup -q -n os-prober
%patch0 -p1 -b .newnsdirfix
%patch1 -p1 -b .macosxdummyfix
%patch2 -p1 -b .mdraidfix
%patch3 -p1 -b .yaboot-parsefix
%patch4 -p1
%patch5 -p1 -b .remove-basename
%patch6 -p1 -b .disable-debug-test
%patch7 -p1
%patch8 -p1 -b .bootpart-name-fix
%patch9 -p1 -b .mounted-partitions-fix
%patch10 -p1 -b .factor-out-logger
%patch11 -p1 

find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;
sed -i -e 's|grub-probe|grub2-probe|g' os-probes/common/50mounted-tests \
     linux-boot-probes/common/50mounted-tests

%build
export CC=gcc
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}

install -m 0755 -p os-prober linux-boot-prober %{buildroot}%{_bindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/newns
install -m 0644 -Dp common.sh %{buildroot}%{_datadir}/%{name}/common.sh

%ifarch m68k
ARCH=m68k
%endif
%ifarch ppc ppc64
ARCH=powerpc
%endif
%ifarch sparc sparc64
ARCH=sparc
%endif
%ifarch %{ix86} x86_64
ARCH=x86
%endif

for probes in os-probes os-probes/mounted os-probes/init \
              linux-boot-probes linux-boot-probes/mounted; do
        install -m 755 -d %{buildroot}%{_libexecdir}/$probes 
        cp -a $probes/common/* %{buildroot}%{_libexecdir}/$probes
        if [ -e "$probes/$ARCH" ]; then 
                cp -a $probes/$ARCH/* %{buildroot}%{_libexecdir}/$probes 
        fi
done
if [ "$ARCH" = x86 ]; then
        install -m 755 -p os-probes/mounted/powerpc/20macosx \
            %{buildroot}%{_libexecdir}/os-probes/mounted
fi

%files
%doc README TODO debian/copyright debian/changelog
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}
%{_var}/lib/%{name}

%changelog
