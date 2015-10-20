Name: os-update
Version: 4.0
Release: 1
Summary: An indicator file of os updates status.

License: BSD 
Source0: updates.xml 

Requires: os-release 

BuildArch:noarch
%description
An indicator file used by isoft-update-client to read out current system updates status

You need change the updates.xml to match updates status when every SP editon release.
%prep
%build
%install
mkdir -p %{buildroot}%{_sysconfdir}/update/
install -m0755 %{SOURCE0} %{buildroot}%{_sysconfdir}/update/

%files
%{_sysconfdir}/update/updates.xml

%changelog
* Fri Oct 16 2015 Cjacker <cjacker@foxmail.com>
- initial build.

