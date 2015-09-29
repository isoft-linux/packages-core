Name:		zd1201-firmware
Version: 	0.14	
Release:	11%{?dist}
Summary:	Firmware for wireless devices based on zd1201 chipset
License:	GPLv2
#wget -O zd1201-0.14-fw.tar.gz 'http://prdownloads.sourceforge.net/linux-lc100020/zd1201-0.14-fw.tar.gz?download'
Source0:	zd1201-0.14-fw.tar.gz
BuildArch:	noarch


%description
This package contains the firmware required to work with the zd1201 chipset.


%prep
%setup -q -n zd1201-0.14-fw
%build
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib/firmware
install -m 0644 *.fw $RPM_BUILD_ROOT/lib/firmware

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/lib/firmware/zd1201*


%changelog
