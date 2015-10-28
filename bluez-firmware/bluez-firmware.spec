Name: bluez-firmware 
Version: 1.2
Release: 2
Summary: Bluetooth firmwares

License: GPLv2
URL: http://www.bluez.org
Source0: http://bluez.sf.net/download/bluez-firmware-%{version}.tar.gz
BuildArch: noarch

%description
%{summary}

%prep
%setup -q

%build
%configure --libdir=/lib
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
/lib/firmware/*

%changelog
* Fri Oct 23 2015 cjacker - 1.2-2
- Rebuild for new 4.0 release


