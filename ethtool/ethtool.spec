Name:		ethtool
Epoch:		2
Version:	4.8
Release:	1%{?dist}
Summary:	Settings tool for Ethernet NICs

License:	GPLv2
#Old URL:	http://sourceforge.net/projects/gkernel/
URL:		http://ftp.kernel.org/pub/software/network/%{name}/

# When using tarball from released upstream version:
# - http://ftp.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.bz2
#
# When generating tarball package from upstream git:
# - git clone git://git.kernel.org/pub/scm/network/ethtool/ethtool.git ethtool-6
# - cd ethtool-6; git checkout 669ba5cadfb15842e90d8aa7ba5a575f7a457b3e
# - cp -f ChangeLog ChangeLog.old; git log > ChangeLog.git
# - rm -rf .git; cd ..; tar cvfz ethtool-6.tar.gz ethtool-6
# - Use the visible date of latest git log entry for %{release} in spec file
Source0:	http://ftp.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz
BuildRequires:	automake, autoconf
Conflicts:      filesystem < 3

%description
This utility allows querying and changing settings such as speed,
port, auto-negotiation, PCI locations and checksum offload on many
network devices, especially of Ethernet devices.

%prep
%setup -q

# Only needed when using upstream git
# aclocal
# autoheader
# automake --gnu --add-missing --copy
# autoconf

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL='install -p' install

%files
%doc AUTHORS ChangeLog* COPYING LICENSE NEWS README
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8*

%changelog
* Thu Dec 08 2016 sulit - 2:4.8-1
- upgrade ethtool to 4.8

* Fri Oct 23 2015 cjacker - 2:4.0-3
- Rebuild for new 4.0 release

