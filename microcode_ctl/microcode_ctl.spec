%define upstream_version 2.1-7

Summary:        Tool to transform and deploy CPU microcode update for x86.
Name:           microcode_ctl
Version:        2.1
Release:        10.1%{?dist}
Epoch:          2
License:        GPLv2+ and Redistributable, no modification permitted
URL:            http://fedorahosted.org/microcode_ctl
Source0:        http://fedorahosted.org/released/microcode_ctl/%{name}-%{upstream_version}.tar.xz
Buildroot:      %{_tmppath}/%{name}-%{version}-root
ExclusiveArch:  %{ix86} x86_64

%description
The microcode_ctl utility is a companion to the microcode driver written
by Tigran Aivazian <tigran@aivazian.fsnet.co.uk>.

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it doesn't reflash your cpu permanently, reboot and it reverts
back to the old microcode.

%prep
%setup -q -n %{name}-%{upstream_version}

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} INSDIR=/usr/sbin install clean

%clean
rm -rf %{buildroot}

%files
/usr/sbin/intel-microcode2ucode
/lib/firmware/*
%doc /usr/share/doc/microcode_ctl/*


%changelog
* Fri Oct 23 2015 cjacker - 2:2.1-10.1
- Rebuild for new 4.0 release

