Name:           iw
Version:        4.1
Release:        2%{?dist}
Summary:        A nl80211 based wireless configuration tool

License:        ISC
URL:            http://www.linuxwireless.org/en/users/Documentation/iw
Source0:        http://www.kernel.org/pub/software/network/iw/iw-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kernel-headers >= 2.6.24 
BuildRequires:  libnl3-devel
BuildRequires:  pkgconfig      

%description
iw is a new nl80211 based CLI configuration utility for wireless devices.
Currently you can only use this utility to configure devices which
use a mac80211 driver as these are the new drivers being written - 
only because most new wireless devices being sold are now SoftMAC.

%prep
%setup -q


%build
export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_datadir}/man/man8/iw.*
%license COPYING

%changelog
* Fri Oct 23 2015 cjacker - 4.1-2
- Rebuild for new 4.0 release

