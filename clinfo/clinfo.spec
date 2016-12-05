Summary: Enumerate OpenCL platforms and devices
Name:    clinfo
Version: 2.1.16.01.12
Release: 1%{?dist}
License: Public Domain
URL:     https://github.com/Oblomov/clinfo

%global tarball %{name}-%{gitversion}.tar.gz
Source0: %{url}/%{name}/archive/%{version}.tar.gz

BuildRequires: opencl-headers ocl-icd-devel


%description
A simple OpenCL application that enumerates all possible platform and
device properties. Inspired by AMD's program of the same name, it is
coded in pure C99 and it tries to output all possible information,
including that provided by platform-specific extensions, and not to
crash on platform-unsupported properties (e.g. 1.2 properties on 1.1
platforms).


%prep
%autosetup


%build
# configure doesn't exist, but we need the exported CFLAGS and friends
%configure || :
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}/%{_bindir}
%{__install} -m0755 clinfo %{buildroot}/%{_bindir}/

mkdir -p %{buildroot}/%{_mandir}/man1
%{__cp} -a man/clinfo.1 %{buildroot}/%{_mandir}/man1/


%files
%doc README LICENSE
%{_bindir}/clinfo
%{_mandir}/man1/clinfo.1.gz

%changelog
* Mon Dec 05 2016 sulit - 2.1.16.01.12-1
- update clinfo to 2.1.16.01.12, rename clinfo versioin name

* Fri Oct 23 2015 cjacker - 0.1-0.8.git20150215.94fdb47
- Rebuild for new 4.0 release

