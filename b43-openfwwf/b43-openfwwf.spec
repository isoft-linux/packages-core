Name:		b43-openfwwf
Version:	5.2
Release:	12%{?dist}
Summary:	Open firmware for some Broadcom 43xx series WLAN chips
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://www.ing.unibs.it/openfwwf/
Source0:	http://www.ing.unibs.it/openfwwf/firmware/openfwwf-%{version}.tar.gz
Source1:	README.openfwwf
Source2:	openfwwf.conf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires:	b43-tools
Requires:	udev
Requires:	module-init-tools


%description
Open firmware for some Broadcom 43xx series WLAN chips.
Currently supported models are 4306, 4311(rev1), 4318 and 4320.


%prep
%setup -q -n openfwwf-%{version}
sed -i s/"-o 0 -g 0"// Makefile
install -p -m 0644 %{SOURCE1} .
install -p -m 0644 %{SOURCE2} .

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/lib/firmware/b43-open
install -p -D -m 0644 openfwwf.conf $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/openfwwf.conf



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING LICENSE README.openfwwf
%dir /lib/firmware/b43-open
/lib/firmware/b43-open/b0g0bsinitvals5.fw
/lib/firmware/b43-open/b0g0initvals5.fw
/lib/firmware/b43-open/ucode5.fw
%{_sysconfdir}/modprobe.d/openfwwf.conf


%changelog
