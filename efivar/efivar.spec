Name:           efivar
Version:        30
Release:        1%{?dist}
Summary:        Tools to manage UEFI variables
License:        LGPLv2.1
URL:            https://github.com/rhinstaller/efivar
Requires:       %{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} x86_64 aarch64

BuildRequires:  popt-devel popt-static git glibc-static
Source0:        https://github.com/rhinstaller/efivar/releases/download/efivar-%{version}/efivar-%{version}.tar.bz2
Patch0:			efivar_use_ar_replace_gcc-ar.patch

%description
efivar provides a simple command line interface to the UEFI variable facility.

%package libs
Summary: Library to manage UEFI variables

%description libs
Library to allow for the simple manipulation of UEFI variables.

%package devel
Summary: Development headers for libefivar
Requires: %{name}-libs = %{version}-%{release}

%description devel
development headers required to use libefivar.

%prep
%setup -q -n %{name}-%{version}
git init
git config user.email "isoft@isoft-linux.org"
git config user.name "isoft"
git add .
git commit -a -q -m "%{version} baseline."
#git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
%patch0 -p1

%build
make libdir=%{_libdir} bindir=%{_bindir} CFLAGS="$RPM_OPT_FLAGS -flto" LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/efivar
%exclude %{_bindir}/efivar-static
%{_mandir}/man1/*

%files devel
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/*.so.*

%changelog
* Thu Dec 08 2016 sulit - 30-1
- build for isoft5.0

