Name:       nss-pem
Version:    1.0.2
Release:    1%{?dist}
Summary:    PEM file reader for Network Security Services (NSS)

License:    MPLv1.1
URL:        https://github.com/kdudka/nss-pem
Source0:    https://github.com/kdudka/nss-pem/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: nss-pkcs11-devel

# make the nss-pem pkg conflict with all nss builds with bundled nss-pem
Conflicts: nss%{?_isa} < 3.25.0-1.2%{?dist}

%description
PEM file reader for Network Security Services (NSS), implemented as a PKCS#11
module.

%prep
%setup -q

%build
mkdir build
cd build
%cmake ../src
make %{?_smp_mflags} VERBOSE=yes

%install
cd build
make install DESTDIR=%{buildroot}

%check
cd build
ctest %{?_smp_mflags} --output-on-failure

%files
%{_libdir}/libnsspem.so
%license COPYING

%changelog
* Tue Jan 03 2017 sulit - 1.0.2-1
- init for isoft

