Summary:	Utilities for managing the XFS filesystem
Name:		xfsprogs
Version:	3.2.3
Release:	3%{?dist}
# Licensing based on generic "GNU GENERAL PUBLIC LICENSE"
# in source, with no mention of version.
# doc/COPYING file specifies what is GPL and what is LGPL
# but no mention of versions in the source.
License:	GPL+ and LGPLv2+
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz
Source1:	xfsprogs-wrapper.h
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool, gettext, libuuid-devel
BuildRequires:	readline-devel, libblkid-devel >= 2.17-0.1.git5e51568
Provides:	xfs-cmds
Obsoletes:	xfs-cmds <= %{version}
Conflicts:	xfsdump < 3.0.1

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.  It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

Refer to the documentation at http://oss.sgi.com/projects/xfs/
for complete details.  This implementation is on-disk compatible
with the IRIX version of XFS.

%package devel
Summary: XFS filesystem-specific headers
Requires: xfsprogs = %{version}-%{release}, libuuid-devel

%description devel
xfsprogs-devel contains the header files needed to develop XFS
filesystem-specific programs.

You should install xfsprogs-devel if you want to develop XFS
filesystem-specific programs,  If you install xfsprogs-devel, you'll
also want to install xfsprogs.

%package qa-devel
Summary: XFS QA filesystem-specific headers
Requires: xfsprogs = %{version}-%{release}
Requires: xfsprogs-devel = %{version}-%{release}

%description qa-devel
xfsprogs-qa-devel contains headers needed to build the xfstests
QA suite.

You should install xfsprogs-qa-devel only if you are interested
in building or running the xfstests QA suite.

%prep
%setup -q

%build
export tagname=CC
%configure \
        --enable-readline=yes	\
	--enable-blkid=yes

# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make V=1 DIST_ROOT=$RPM_BUILD_ROOT install install-dev install-qa \
	PKG_ROOT_SBIN_DIR=%{_sbindir} PKG_ROOT_LIB_DIR=%{_libdir}

# nuke .la files, etc
rm -f $RPM_BUILD_ROOT/{%{_lib}/*.{la,a,so},%{_libdir}/*.{la,a}}
chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/libhandle.so.*.*.*

# remove non-versioned docs location
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/xfsprogs/

# ugly hack to allow parallel install of 32-bit and 64-bit -devel packages:
%define multilib_arches %{ix86} x86_64 ppc ppc64 s390 s390x %{sparc}

%ifarch %{multilib_arches}
mv -f $RPM_BUILD_ROOT%{_includedir}/xfs/platform_defs.h \
      $RPM_BUILD_ROOT%{_includedir}/xfs/platform_defs-%{_arch}.h
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/xfs/platform_defs.h
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES doc/COPYING doc/CREDITS README
%{_libdir}/*.so.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_mandir}/man3/*
%dir %{_includedir}/xfs
%{_includedir}/xfs/handle.h
%{_includedir}/xfs/jdm.h
%{_includedir}/xfs/linux.h
%ifarch %{multilib_arches}
%{_includedir}/xfs/platform_defs-%{_arch}.h
%endif
%{_includedir}/xfs/platform_defs.h
%{_includedir}/xfs/xfs.h
%{_includedir}/xfs/xfs_fs.h
%{_includedir}/xfs/xfs_types.h
%{_includedir}/xfs/xqm.h
%{_libdir}/*.so

%files qa-devel
%defattr(-,root,root)
%{_includedir}/xfs/atomic.h
%{_includedir}/xfs/bitops.h
%{_includedir}/xfs/cache.h
%{_includedir}/xfs/hlist.h
%{_includedir}/xfs/kmem.h
%{_includedir}/xfs/libxfs.h
%{_includedir}/xfs/libxlog.h
%{_includedir}/xfs/list.h
%{_includedir}/xfs/parent.h
%{_includedir}/xfs/radix-tree.h
%{_includedir}/xfs/swab.h
%{_includedir}/xfs/xfs_ag.h
%{_includedir}/xfs/xfs_alloc.h
%{_includedir}/xfs/xfs_alloc_btree.h
%{_includedir}/xfs/xfs_arch.h
%{_includedir}/xfs/xfs_attr_leaf.h
%{_includedir}/xfs/xfs_attr_remote.h
%{_includedir}/xfs/xfs_attr_sf.h
%{_includedir}/xfs/xfs_bit.h
%{_includedir}/xfs/xfs_bmap.h
%{_includedir}/xfs/xfs_bmap_btree.h
%{_includedir}/xfs/xfs_btree.h
%{_includedir}/xfs/xfs_btree_trace.h
%{_includedir}/xfs/xfs_cksum.h
%{_includedir}/xfs/xfs_da_btree.h
%{_includedir}/xfs/xfs_da_format.h
%{_includedir}/xfs/xfs_dinode.h
%{_includedir}/xfs/xfs_dir2.h
%{_includedir}/xfs/xfs_format.h
%{_includedir}/xfs/xfs_ialloc.h
%{_includedir}/xfs/xfs_ialloc_btree.h
%{_includedir}/xfs/xfs_inode_buf.h
%{_includedir}/xfs/xfs_inode_fork.h
%{_includedir}/xfs/xfs_inum.h
%{_includedir}/xfs/xfs_log_format.h
%{_includedir}/xfs/xfs_log_recover.h
%{_includedir}/xfs/xfs_metadump.h
%{_includedir}/xfs/xfs_quota_defs.h
%{_includedir}/xfs/xfs_sb.h
%{_includedir}/xfs/xfs_shared.h
%{_includedir}/xfs/xfs_trace.h
%{_includedir}/xfs/xfs_trans_resv.h
%{_includedir}/xfs/xfs_trans_space.h

%changelog
* Fri Oct 23 2015 cjacker - 3.2.3-3
- Rebuild for new 4.0 release

