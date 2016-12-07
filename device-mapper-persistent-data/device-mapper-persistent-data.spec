Summary: Device-mapper Persistent Data Tools
Name: device-mapper-persistent-data
Version: 0.6.3
Release: 1%{?dist}
License: GPLv3+
URL: https://github.com/jthornber/thin-provisioning-tools
Source0: https://github.com/jthornber/thin-provisioning-tools/archive/v%{version}.tar.gz
# Source1: https://github.com/jthornber/thin-provisioning-tools/archive/v%{version}.tar.gz
BuildRequires: autoconf, expat-devel, libaio-devel, libstdc++-devel, boost-devel
Requires: expat
Patch0: device-mapper-persistent-data-0.4.1-bz1085620.patch
Patch1: device-mapper-persistent-data-0.4.1-missing-man-pages.patch
Patch2: device-mapper-persistent-data-avoid-strip.patch
Patch3: device-mapper-persistent-data-add-era_restore-and-cache_metadata_size-man-pages.patch

%description
thin-provisioning-tools contains check,dump,restore,repair,rmap
and metadata_size tools to manage device-mapper thin provisioning
target metadata devices; cache check,dump,metadata_size,restore
and repair tools to manage device-mapper cache metadata devices
are included and era check, dump, restore and invalidate to manage
snapshot eras

%prep
%setup -q -n thin-provisioning-tools-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
echo %{version}-%{release} > VERSION

%build
autoconf
%configure --with-optimisation=
make %{?_smp_mflags} V=

%install
make DESTDIR=%{buildroot} MANDIR=%{_mandir} install

%clean

%files
%doc COPYING README.md
%{_mandir}/man8/cache_check.8.gz
%{_mandir}/man8/cache_dump.8.gz
%{_mandir}/man8/cache_restore.8.gz
%{_mandir}/man8/cache_repair.8.gz
%{_mandir}/man8/era_check.8.gz
%{_mandir}/man8/era_dump.8.gz
%{_mandir}/man8/era_invalidate.8.gz
%{_mandir}/man8/thin_check.8.gz
%{_mandir}/man8/thin_dump.8.gz
%{_mandir}/man8/thin_metadata_size.8.gz
%{_mandir}/man8/thin_restore.8.gz
%{_mandir}/man8/thin_repair.8.gz
%{_mandir}/man8/thin_rmap.8.gz
%{_mandir}/man8/thin_delta.8.gz
%{_mandir}/man8/thin_ls.8.gz
%{_mandir}/man8/thin_trim.8.gz
%{_sbindir}/pdata_tools
%{_sbindir}/cache_check
%{_sbindir}/cache_dump
%{_sbindir}/cache_metadata_size
%{_sbindir}/cache_restore
%{_sbindir}/cache_repair
%{_sbindir}/era_check
%{_sbindir}/era_dump
%{_sbindir}/era_restore
%{_sbindir}/era_invalidate
%{_sbindir}/thin_check
%{_sbindir}/thin_dump
%{_sbindir}/thin_metadata_size
%{_sbindir}/thin_restore
%{_sbindir}/thin_repair
%{_sbindir}/thin_rmap
%{_sbindir}/thin_delta
%{_sbindir}/thin_ls
%{_sbindir}/thin_trim


%changelog
* Wed Dec 07 2016 sulit - 0.6.3-1
- upgrade device-mapper-persistent-data to 0.6.3
- add avoid-strip patch

* Fri Oct 23 2015 cjacker - 0.4.1-4
- Rebuild for new 4.0 release

