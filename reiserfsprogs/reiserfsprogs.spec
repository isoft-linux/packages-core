Name: reiserfsprogs
Version: 3.6.24
Release: 12%{?dist}
Summary: Tools for creating, repairing, and debugging ReiserFS filesystems
URL: http://ftp.kernel.org/pub/linux/utils/fs/reiserfs/
Source0: https://www.kernel.org/pub/linux/kernel/people/jeffm/reiserfsprogs/v%{version}/reiserfsprogs-%{version}.tar.xz
License: GPLv2 with exceptions

BuildRequires: e2fsprogs-devel
BuildRequires: libuuid-devel

%description
The reiserfs-utils package contains a number of utilities for
creating, checking, modifying, and correcting any inconsistencies in
ReiserFS filesystems, including reiserfsck (used to repair filesystem
inconsistencies), mkreiserfs (used to initialize a partition to
contain an empty ReiserFS filesystem), debugreiserfs (used to examine
the internal structure of a filesystem, to manually repair a corrupted
filesystem, or to create test cases for reiserfsck), and some other
ReiserFS filesystem utilities.

You should install the reiserfs-utils package if you want to use
ReiserFS on any of your partitions.

%prep
%setup -q

%build
#-std=gnu90 fix build with gcc5

export CFLAGS="$RPM_OPT_FLAGS -std=gnu90" CXXFLAGS="$RPM_OPT_FLAGS"
find . -name "config.cache" |xargs rm -f

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
mv -f $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 debugreiserfs/debugreiserfs.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 fsck/reiserfsck.8 $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 mkreiserfs/mkreiserfs.8 $RPM_BUILD_ROOT%{_mandir}/man8

( cd $RPM_BUILD_ROOT/sbin
  ln -fs mkreiserfs mkfs.reiserfs
  ln -fs reiserfsck fsck.reiserfs )

%files
%defattr(-,root,root,-)
/sbin/debugreiserfs
/sbin/mkreiserfs
/sbin/reiserfsck
/sbin/resize_reiserfs
/sbin/reiserfstune
/sbin/mkfs.reiserfs
/sbin/fsck.reiserfs
/sbin/debugfs.reiserfs
/sbin/tunefs.reiserfs
%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 23 2015 cjacker - 3.6.24-12
- Rebuild for new 4.0 release

