%global distroname %(source /etc/os-release; echo ${REDHAT_SUPPORT_PRODUCT})

Summary: The skeleton package which defines a simple %{distroname} system
Name: basesystem
Version: 11
Release: 1%{?dist}
License: Public Domain
Group: System Environment/Base
Requires(pre): setup filesystem
BuildArch: noarch

%description
Basesystem defines the components of a basic %{distroname} system 
(for example, the package installation order to use during bootstrapping).
Basesystem should be in every installation of a system, and it
should never be removed.

%prep

%build

%install

%clean

%files
%defattr(-,root,root,-)

%changelog
