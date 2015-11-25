%define rpmver 4.13.0
%define bdbver  6.1.23

Summary: The RPM package management system
Name: rpm
Version: %{rpmver} 
Release: 32
Url: http://www.rpm.org/
License: GPLv2+
Source0: http://rpm.org/releases/rpm-4.13.x/%{name}-%{version}-rc1.tar.bz2
Source1: http://download.oracle.com/berkeley-db/db-%{bdbver}.tar.gz

#A script for strip debug infos, SHOULD NOT be used, just keep it here.
Source20: rpmclean

#isoft rpmrc and macros
Source30: rpmrc.isoft
Source31: macros.isoft


# Disable autoconf config.site processing (#962837)
Patch1: rpm-4.11.x-siteconfig.patch
# man-pages pkg owns all the localized man directories
Patch3: rpm-4.9.90-no-man-dirs.patch
# Temporary band-aid for rpm2cpio whining on payload size mismatch (#1142949)
Patch5: rpm-4.12.0-rpm2cpio-hack.patch

# Patches already upstream:
Patch100: rpm-4.12.90-braces-expansion.patch
Patch101: rpm-4.12.90-Fix-compressed-patches.patch
Patch102: rpm-4.12.90-fix-macro-warning.patch
Patch103: rpm-4.12.90-modify-rpmisglob.patch
Patch104: rpm-4.12.90-try-unglobbed.patch
Patch105: rpm-4.12.90-show-filetriggers.patch

# These are not yet upstream
Patch302: rpm-4.7.1-geode-i686.patch
# Probably to be upstreamed in slightly different form
Patch304: rpm-4.9.1.1-ld-flags.patch
# Compressed debuginfo support (#833311)
Patch305: rpm-4.10.0-dwz-debuginfo.patch
# Minidebuginfo support (#834073)
Patch306: rpm-4.10.0-minidebuginfo.patch
# Fix CRC32 after dwz (#971119)
Patch307: rpm-4.11.1-sepdebugcrcfix.patch
# Fix race condidition where unchecked data is exposed in the file system
Patch308: rpm-4.12.0.x-CVE-2013-6435.patch
# Add check against malicious CPIO file name size
Patch309: rpm-4.12.0.x-CVE-2014-8118.patch


Patch1300: rpm-default-patch-fuzz-tune.patch
Patch1305: rpm-enable-unpackaged-file.patch
#It's already in macros.isoft
Patch1308: rpm-enable-xz-payload.patch
Patch1309: rpm-never-lib64.patch
Patch1310: rpm-remove-la.patch
#unused, if build debug info, it will called after debuginfo extracted. 
Patch1311: rpm-enable-brp-strip-shared.patch
Patch1500: rpm-macro-add-python3.patch

#iSOFT App isolation support
Patch2000: 0001-isoftapp-skeleton.patch
# Keep silent DB
Patch2001: 0002-db-quite.patch

Requires: popt >= 1.10.2.1
Requires: coreutils
#example, findlang.sh requires a gnu sed
Requires: sed
Requires: librpm = %{version}-%{release}

BuildRequires: automake
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: zlib-devel
BuildRequires: nss-devel
BuildRequires: libcap-devel
BuildRequires: binutils-devel

# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: ncurses-devel
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
BuildRequires: python3-devel

BuildRequires: dbus-devel

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package -n librpm
Summary:  Libraries for manipulating RPM packages
License: GPLv2+ and LGPLv2+ with exceptions

%description -n librpm
This package contains the RPM shared libraries.

%package build
Summary: Scripts and executable programs used to build packages
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
Requires: librpm = %{version}-%{release}

%description -n python-rpm
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.



%package -n python3-rpm
Summary: Python 3 bindings for apps which will manipulate RPM packages
Requires: librpm = %{version}-%{release}

%description -n python3-rpm
The rpm-python3 package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3
programs that will manipulate RPM packages and databases.

%prep
%setup -q -n %{name}-%{version}-rc1 -a 1
%patch1 -p1
%patch3 -p1
%patch5 -p1

%patch302 -p1
%patch304 -p1
%patch305 -p1
%patch306 -p1
%patch307 -p1
%patch308 -p1
%patch309 -p1


%patch1300 -p1
%patch1305 -p1
%patch1308 -p1
%patch1309 -p1
%patch1310 -p1
#%patch1311 -p1
%patch1500 -p1

%patch2000 -p1
%patch2001 -p1

ln -s db-%{bdbver} db

%build
#=========================================
#check the build environment rpm macros.
#If rpm in build environment did not provide the correct macros,
#Stop the building.

_ARCH=`rpm --eval %{_arch}`
_HOSTNAME=`rpm --eval %{_host}`
_HOSTVENDOR=`rpm --eval %{_host_vendor}`
_TARGETPLATFORM=`rpm --eval %{_target_platform}`

if [ x"$_HOSTVENDOR" == x"isoft" ]; then
   echo "'_host_vendor' macro is as what we expected."
else
   echo "'_host_vendor' rpm macro is wrong, building terminated."
   exit 1
fi

if [ x"$_TARGETPLATFORM" == x"$_ARCH""-isoft-linux" ]; then
   echo "'_target_platform' macro is as what we expected."
else
   echo "'_target_platform' macro is wrong, building terminated."
   exit 1
fi

if [ x"$_HOSTNAME" == x"$_ARCH""-isoft-linux-gnu" ]; then
   echo "'_host' macro is as what we expected."
else
   echo "'_host' rpm macro is wrong, building terminated."
   exit 1
fi

#=========================================


CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss` -DLUA_COMPAT_APIINTCASTS"
CFLAGS="$RPM_OPT_FLAGS %{?sanitizer_flags} -DLUA_COMPAT_APIINTCASTS"
export CPPFLAGS CFLAGS LDFLAGS
#autoreconf -i
%configure \
    --with-archive \
    --with-lua \
    --with-cap \
    --enable-plugins \
    --enable-python \
    --with-vendor=isoft

make %{?_smp_mflags}

pushd python
%{__python} setup.py build
%{__python3} setup.py build
popd


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

# We need to build with --enable-python for the self-test suite, but we
# actually package the bindings built with setup.py (#531543#c26)
rm -rf $RPM_BUILD_ROOT/%{python_sitearch}
pushd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


#isoft rpmrc/macros
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rpm/isoft
install -m 0644 %{SOURCE30} $RPM_BUILD_ROOT%{_libdir}/rpm/isoft/rpmrc
install -m 0644 %{SOURCE31} $RPM_BUILD_ROOT%{_libdir}/rpm/isoft/macros


mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
mkdir -p $RPM_BUILD_ROOT/var/lib/isoft-app
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Obsoletename \
    Packages Providename Requirename Triggername Sha1header Sigmd5 \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
    touch $RPM_BUILD_ROOT/var/lib/isoft-app/$dbi
done


install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT/%{_bindir}/rpmclean

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d
echo "r /var/lib/rpm/__db.*" > ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d/rpm.conf
echo "r /var/lib/isoft-app/__db.*" > ${RPM_BUILD_ROOT}%{_sysconfdir}/tmpfiles.d/isoft-app.conf


#do not import so many perl deps.
#chmod 0644 $RPM_BUILD_ROOT%{_libdir}/rpm/perldeps.pl

rm -rf   $RPM_BUILD_ROOT%{_mandir}/{fr,ja,ko,pl,ru,sk}

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

#=========================================
#check _host_vendor _host macros in %{buildroot}/usr/lib/rpm/macros
_VENDOR_IN_FILE=`grep "^"%"_host_vendor" %{buildroot}%{_libdir}/rpm/macros |awk -F ' ' '{print $2}'`
if [ x"$_VENDOR_IN_FILE" != x"isoft" ]; then
   echo "The '_host_vendor' in <LIBDIR>/rpm/macros generated by this build is NOT as what we expected."
   exit 1
fi
#=========================================



%clean
rm -rf $RPM_BUILD_ROOT

%post -n librpm -p /sbin/ldconfig 
%postun -n librpm -p /sbin/ldconfig


%files -f %{name}.lang
%{_sysconfdir}/tmpfiles.d/rpm.conf
%{_sysconfdir}/tmpfiles.d/isoft-app.conf
%dir %{_sysconfdir}/rpm
%attr(0755, root, root) %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*
%attr(0755, root, root) %dir /var/lib/isoft-app
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/isoft-app/*

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

%{_libdir}/rpm/isoft/rpmrc
%{_libdir}/rpm/isoft/macros

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
%{_libdir}/rpm/sepdebugcrcfix
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
%{python_sitearch}/rpm_python-*.egg-info

%files -n python3-rpm
%defattr(-,root,root)
%{python3_sitearch}/rpm
%{python3_sitearch}/rpm_python-*.egg-info


%changelog
* Wed Nov 25 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add rpmSpecBuildISoftApp for converting src rpm to bin rpm.
- Fix fileName is NULL issue for packageBinaries.

* Mon Nov 23 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Fix closing already-closed cursor issue.

* Thu Nov 19 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Enable %_isoftapp macro by default.
- Fix rpmdbNextIteratorISoftApp forget to close db issue.

* Wed Nov 18 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Keep quite please Berkeley DB.

* Tue Nov 17 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Public openDatabase and rpmdbClose for isoft-package-installer.

* Thu Nov 12 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- rpm only rpmpsPrint problem into console
- but isoft-package-installer need probPtr to emit detail error info 
- add probPtr for rpmInstallISoftApp interface
- add rpmpsToChunk and chunk_t struct

* Wed Nov 11 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Fix unsatisfiedDepend dbOpened issue.
- Fix open too many db issue.
- Fix rpmInstallISoftApp thread unsafe issue.

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 4.13.0-20
- Rebuild with python 3.5

* Wed Nov 04 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- By default %_isoftapp macro is N, editable in /usr/lib/rpm/isoft/macros
- Fix conflict issue.

* Tue Nov 03 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add rpmdbCountProvides API for verifying isoft-app db.
- Fix vendor in file check issue.
- Fix openDatabase usage issue.

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 4.13.0-15
- Add test of _target_platform macro

* Mon Nov 02 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Fix update package without erase old one issue.
- Fix verify isoftapp issue.
- Keep silent DB.

* Mon Nov 02 2015 Cjacker <cjacker@foxmail.com> - 4.13.0-8
- Add macro check of environment and build results

* Fri Oct 30 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add rpmtsSetMacro by fujiang.
- Add isoftapp macro support.
- Fix verify, install, update issue.
- Fix already installed for both osdb and isoft-appdb issue.

* Fri Oct 23 2015 cjacker - 4.13.0-4
- Rebuild for new 4.0 release

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 4.13.0-3
- Add debuginfo support in macros.isoft

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 4.13.0-2
- Add P1311, fix not involk brp-strip-shared issue.

* Thu Sep 24 2015 LeslieZhai <xiang.zhai@i-soft.com.cn>
- add patch2000, support isoft-app seperately app db.

