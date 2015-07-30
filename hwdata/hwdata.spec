Name: hwdata
Summary: Hardware identification and configuration data
Version: 0.278
Release: 2
License: GPLv2+
Group:  Core/Runtime/Data 
Source: https://fedorahosted.org/releases/h/w/%{name}/%{name}-%{version}.tar.bz2
URL:    http://git.fedorahosted.org/git/hwdata.git
BuildArch: noarch

%description
hwdata contains various hardware identification and configuration data,
such as the pci.ids and usb.ids databases.

%prep
%setup -q

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_prefix}/lib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_datadir}/%{name}
%{_prefix}/lib/modprobe.d/dist-blacklist.conf
%{_datadir}/%{name}/*

%changelog
* Wed Oct 15 2014 Cjacker <cjacker@gmail.com>
- review and update.
