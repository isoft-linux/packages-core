%define snap 2007-03-19
Name:		zd1211-firmware
Version:	1.4
Release:	11%{?dist}
Summary:	Firmware for wireless devices based on zd1211 chipset
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://zd1211.wiki.sourceforge.net
Source0:	http://downloads.sourceforge.net/zd1211/zd1211-firmware-%{version}.tar.bz2
Patch0:		zd1211-firmware-1.4-build__from_headers.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch


%description
This package contains the firmware required to work with the zd1211 chipset.


%prep
%setup -q -n %{name}
%patch0 -p1
sed -i 's/\r//' *.h

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install FW_DIR=$RPM_BUILD_ROOT/lib/firmware/zd1211 


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING
%dir /lib/firmware/zd1211
/lib/firmware/zd1211/*


%changelog
