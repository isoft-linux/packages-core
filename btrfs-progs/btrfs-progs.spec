Name:		btrfs-progs
Version:    4.0.1 
Release:	1
Summary:	Userspace programs for btrfs

Group:	    Core/Runtime/Utility
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz

BuildRequires:	e2fsprogs-devel, libuuid-devel, zlib-devel
BuildRequires:	libacl-devel, libblkid-devel, lzo-devel
Requires:   libbtrfs = %{version}-%{release}

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.


%package -n libbtrfs
Summary:    btrfs filesystem-specific libraries and headers
Group:      Core/Runtime/Library

%description -n libbtrfs
%{summary}

%package -n libbtrfs-devel
Summary:	btrfs filesystem-specific libraries and headers
Group:		Core/Development/Library
Requires:	libbtrfs = %{version}-%{release}

%description -n libbtrfs-devel
libbtrfs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

You should install libbtrfs-devel if you want to develop
btrfs filesystem-specific programs.

%prep
%setup -q -n %{name}-v%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir}/btrfs install DESTDIR=$RPM_BUILD_ROOT
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sbindir}/btrfsck
%{_sbindir}/mkfs.btrfs
%{_sbindir}/fsck.btrfs
%{_sbindir}/btrfs-debug-tree
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-zero-log
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-show-super
%{_sbindir}/btrfs-select-super
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n libbtrfs
%{_libdir}/libbtrfs.so.0*

%files -n libbtrfs-devel
%{_includedir}/*
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfs.a

%changelog
* Sat Dec 21 2013 Cjacker <cjacker@gmail.com>
- New upstream snapshot

