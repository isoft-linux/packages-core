%define rpmver 4.12.0.1
%define bdbver  6.1.23

Summary: The RPM package management system
Name: rpm
Version: %{rpmver} 
Release: 1
Group:  Core/Runtime/Utility 
Url: http://www.rpm.org/
License: GPLv2+
Source0: http://rpm.org/releases/rpm-4.12.x/%{name}-%{version}.tar.bz2
Source1: http://download.oracle.com/berkeley-db/db-%{bdbver}.tar.gz

#A script for strip debug infos
Source20: rpmclean

Patch300: rpm-default-patch-fuzz-tune.patch
Patch305: rpm-enable-unpackaged-file.patch
Patch308: rpm-enable-xz-payload.patch
Patch309: rpm-never-lib64.patch
Patch310: rpm-remove-la.patch
Patch500: rpm-macro-add-python3.patch

Patch600: rpm-lua-5.3.patch

Requires: popt >= 1.10.2.1
Requires: coreutils
#example, findlang.sh requires a gnu sed
Requires: sed
Requires: librpm = %{version}-%{release}

BuildRequires: zlib-devel
BuildRequires: nss-devel
BuildRequires: libcap-devel

# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: xz-devel >= 4.999.8
#for elfdeps
BuildRequires: libelfutils-devel >= 0.159
BuildRequires: pkgconfig
#for lua script support
BuildRequires: lua-devel
#for rpm2archive
BuildRequires: libarchive-devel
#for rpm python module
BuildRequires: python-devel

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package -n librpm
Summary:  Libraries for manipulating RPM packages
Group:  Core/Runtime/Library 
License: GPLv2+ and LGPLv2+ with exceptions

%description -n librpm
This package contains the RPM shared libraries.

%package build
Summary: Scripts and executable programs used to build packages
Group:  Core/Development/Utility 
Requires: rpm = %{version}-%{release}
Requires: elfutils binutils
Requires: findutils sed grep gawk diffutils file patch
Requires: unzip gzip bzip2 cpio xz
Requires: pkgconfig

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.


%package -n librpm-devel
Summary:  Development files for manipulating RPM packages
Group: Core/Development/Library
License: GPLv2+ and LGPLv2+ with exceptions
Requires: librpm = %{version}-%{release}
Requires: popt-devel

%description -n librpm-devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package -n python-rpm
Summary: Python bindings for apps which will manipulate RPM packages
Group:  Core/Runtime/Library
Requires: librpm = %{version}-%{release}

%description -n python-rpm
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%prep
%setup -q -n %{name}-%{version} -a 1
%patch300 -p1
%patch305 -p1 -b .unpackaged
%patch308 -p1
%patch309 -p1
%patch310 -p1
%patch500 -p1
%patch600 -p1

ln -s db-%{bdbver} db

%build
CPPFLAGS="$CPPFLAGS -I/usr/include/nss3 -I/usr/include/nspr4"
CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS CFLAGS LDFLAGS
%configure \
    --with-archive \
    --with-lua \
    --with-cap \
    --enable-plugins \
    --enable-python \
    --with-vendor=pure64

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done


install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT/%{_bindir}/rpmclean

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d/rpm.conf


#do not import so many perl deps.
chmod 0644 $RPM_BUILD_ROOT%{_libdir}/rpm/perldeps.pl

rm -rf   $RPM_BUILD_ROOT%{_mandir}/{fr,ja,ko,pl,ru,sk}

%find_lang %{name}

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -n librpm -p /sbin/ldconfig 
%postun -n librpm -p /sbin/ldconfig


%files -f %{name}.lang
%{_sysconfdir}/tmpfiles.d/rpm.conf
%dir %{_sysconfdir}/rpm
%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*

/bin/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpm2archive
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{_bindir}/rpmsign
%{_bindir}/rpmclean

%{_mandir}/man8/rpmsign.8*
%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*

%attr(0755, root, root) %dir %{_libdir}/rpm 
%{_libdir}/rpm/macros
%{_libdir}/rpm/rpmpopt*
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/rpmdb_*
%{_libdir}/rpm/rpm.daily
%{_libdir}/rpm/rpm.supp
%{_libdir}/rpm/rpm.log
%{_libdir}/rpm/rpm2cpio.sh
%{_libdir}/rpm/tgpg
%{_libdir}/rpm/platform

%files build
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*
%{_mandir}/man8/rpmspec.8*

%{_libdir}/rpm/brp-*
%{_libdir}/rpm/check-*
%{_libdir}/rpm/debugedit
%{_libdir}/rpm/find-debuginfo.sh
%{_libdir}/rpm/find-lang.sh
%{_libdir}/rpm/*provides*
%{_libdir}/rpm/*requires*
%{_libdir}/rpm/*deps*
%{_libdir}/rpm/*.prov
%{_libdir}/rpm/*.req
%{_libdir}/rpm/config.*
%{_libdir}/rpm/mkinstalldirs
%{_libdir}/rpm/macros.*
%{_libdir}/rpm/fileattrs

%files -n librpm
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_libdir}/rpm-plugins
%{_libdir}/librpmbuild.so.*
%{_libdir}/librpmsign.so.*


%files -n librpm-devel
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph
%{_libdir}/librp*[a-z].so
%{_libdir}/pkgconfig/rpm.pc
%{_includedir}/rpm

%files -n python-rpm
%{python_sitearch}/rpm

