Name:           rfkill
Version:        0.5
Release:        7%{?dist}
Summary:        A tool for enabling and disabling wireless devices

License:        ISC
URL:            http://www.linuxwireless.org/en/users/Documentation/rfkill
Source0:        https://www.kernel.org/pub/software/network/rfkill/rfkill-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
rfkill is a simple tool for accessing the Linux rfkill device interface,
which is used to enable and disable wireless networking devices, typically
WLAN, Bluetooth and mobile broadband.

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT} PREFIX='' MANDIR=%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/sbin/rfkill
%{_mandir}/man8/*
%license COPYING
%doc README


%changelog
* Fri Oct 23 2015 cjacker - 0.5-7
- Rebuild for new 4.0 release

