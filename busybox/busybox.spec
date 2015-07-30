Summary: busybox
Name: busybox
Version: 1.23.2
Release: 1
License: GPLv2+
Group:   Core/Runtime/Utility
Source0: busybox-%{version}.tar.bz2
Source1: nologin.c

Source10: busyboxconfig

Patch0:	busybox-uname-is-not-gnu.patch
Patch1:	bb-app-location.patch
Patch2:	loginutils-sha512.patch
Patch3:	udhcpc-discover-retries.patch
Patch9:	0001-ifupdown-use-x-hostname-NAME-with-udhcpc.patch
Patch16:	0001-diff-add-support-for-no-dereference.patch
Patch17:	busybox-header1.patch
Patch18:    busybox-fix-clang-make-flags.patch

BuildRequires: kernel-headers

%description
busybox 
%prep
%setup -q
cp %{SOURCE1} loginutils
%patch0  -p1
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch9  -p1

%patch16 -p1
%patch17 -p1

%patch18 -p1

%build
cp %{SOURCE10} ./.config
sed -i -e "s/CONFIG_EXTRA_COMPAT=y/CONFIG_EXTRA_COMPAT=n/" .config
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
/usr/bin/busybox
