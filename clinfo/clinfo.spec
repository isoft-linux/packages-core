%global commit 94fdb47af528d24a08f1549efe7ab79bcdc5f878
%global commitdate 20150215
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitversion .git%{commitdate}.%{shortcommit}

Summary: Enumerate OpenCL platforms and devices
Name:    clinfo
Version: 0.1
Release: 0.7%{?gitversion}%{?dist}
License: Public Domain
Group:   System Environment/Libraries
URL:     https://github.com/Oblomov/clinfo

%global tarball %{name}-%{gitversion}.tar.gz
Source0: https://github.com/Oblomov/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires: opencl-headers ocl-icd-devel


%description
A simple OpenCL application that enumerates all possible platform and
device properties. Inspired by AMD's program of the same name, it is
coded in pure C99 and it tries to output all possible information,
including that provided by platform-specific extensions, and not to
crash on platform-unsupported properties (e.g. 1.2 properties on 1.1
platforms).


%prep
%setup -q -n %{name}-%{commit}


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
