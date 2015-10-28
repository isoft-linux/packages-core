Summary: A utility for displaying and/or setting hard disk parameters
Name: hdparm
Version: 9.48
Release: 2%{?dist}
License: BSD
URL:    http://sourceforge.net/projects/hdparm/
Source: http://download.sourceforge.net/hdparm/hdparm-%{version}.tar.gz
Patch2: %{name}-9.43-ditch_dead_code.patch
Patch3: %{name}-9.43-close_fd.patch
Patch4: %{name}-9.43-get_geom.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Hdparm is a useful system utility for setting (E)IDE hard drive
parameters.  For example, hdparm can be used to tweak hard drive
performance and to spin down hard drives for power conservation.

%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} STRIP=/bin/true LDFLAGS=

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
install -c -m 755 hdparm $RPM_BUILD_ROOT/sbin/hdparm
install -c -m 644 hdparm.8 $RPM_BUILD_ROOT/%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc hdparm.lsm Changelog LICENSE.TXT README.acoustic TODO
/sbin/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Fri Oct 23 2015 cjacker - 9.48-2
- Rebuild for new 4.0 release

