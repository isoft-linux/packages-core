Name:           mpkg-minimal
Version:        1.0
Release:        1%{?dist}
Summary:        Script to allow mpkg fetch to work

Group:          Applications/System
License:        GPLv2+
URL:            http://git.isoft.zhcn.cc/version-4/%{name}
Source0:	http://pkg.isoft.zhcn.cc/repo/pkgs/%{name}/%{name}-%{version}.tar.xz/80cc4c096b166e4363645becbcefdd81/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       curl, coreutils, rpmdevtools

Conflicts:      fedpkg, mpkg


%description
Script for use in Koji to allow sources to be fetched

%prep
%setup -q

%build

%install
make install PREFIX=%{_prefix}

%files
%doc README.md LICENSE
%{_bindir}/mpkg

%changelog
