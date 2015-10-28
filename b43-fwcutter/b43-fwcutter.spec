Name:           b43-fwcutter
Version:        019
Release:        6%{?dist}
Summary:        Firmware extraction tool for Broadcom wireless driver

License:        BSD
URL:            http://bues.ch/b43/fwcutter/
Source0:        http://bues.ch/b43/fwcutter/%{name}-%{version}.tar.bz2
Source1:        README.too
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package contains the 'b43-fwcutter' tool which is used to
extract firmware for the Broadcom network devices.

See the README.too file shipped in the package's documentation for
instructions on using this tool.

%prep
%setup -q

cp %{SOURCE1} .

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m0755 b43-fwcutter $RPM_BUILD_ROOT%{_bindir}/b43-fwcutter
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m0644 b43-fwcutter.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/b43-fwcutter
%{_mandir}/man1/*
%license COPYING
%doc README README.too

%changelog
* Fri Oct 23 2015 cjacker - 019-6
- Rebuild for new 4.0 release

