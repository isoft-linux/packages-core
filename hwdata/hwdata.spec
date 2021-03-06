Name: hwdata
Summary: Hardware identification and configuration data
Version: 0.295
Release: 1
License: GPLv2+
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
* Thu Dec 15 2016 sulit - 0.295-1
- upgrade hwdata to 0.295

* Fri Oct 23 2015 cjacker - 0.282-3
- Rebuild for new 4.0 release

* Mon Oct 05 2015 Cjacker <cjacker@foxmail.com>
- update to 282

* Mon Sep 07 2015 Cjacker <cjacker@foxmail.com>
- update to 281

* Wed Oct 15 2014 Cjacker <cjacker@gmail.com>
- review and update.
