Name: busybox
Summary: BusyBox combines tiny versions of many common UNIX utilities into a single small executable 
Version: 1.24.0
Release: 1
License: GPLv2+
Source0: busybox-%{version}.tar.bz2
Source1: nologin.c

Source10: busyboxconfig

Patch1:	bb-app-location.patch
Patch2:	loginutils-sha512.patch
Patch3:	udhcpc-discover-retries.patch
Patch9:	0001-ifupdown-use-x-hostname-NAME-with-udhcpc.patch
Patch16: 0001-diff-add-support-for-no-dereference.patch
Patch17: busybox-header1.patch
Patch18: busybox-fix-clang-make-flags.patch

BuildRequires: kernel-headers gcc glibc-devel

%description
BusyBox combines tiny versions of many common UNIX utilities into a single
small executable.  It provides minimalist replacements for most of the
utilities you usually find in bzip2, coreutils, dhcp, diffutils, e2fsprogs,
file, findutils, gawk, grep, inetutils, less, modutils, net-tools, procps,
sed, shadow, sysklogd, sysvinit, tar, util-linux, and vim.  The utilities
in BusyBox often have fewer options than their full-featured cousins;
however, the options that are included provide the expected functionality
and behave very much like their larger counterparts.

%prep
%setup -q
cp %{SOURCE1} loginutils
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch9  -p1

%patch16 -p1
%patch17 -p1

%patch18 -p1

cp %{SOURCE10} ./.config
sed -i -e "s/CONFIG_EXTRA_COMPAT=y/CONFIG_EXTRA_COMPAT=n/" .config

%build
make oldconfig
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 0755 busybox $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/busybox --install -s

%files 
%defattr(-, root, root, -)
%{_bindir}/busybox
