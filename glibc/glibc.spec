%define glibcversion 2.21
%define glibcrelease 11

Summary: The GNU libc libraries.
Name: glibc
Version: %{glibcversion}
Release: %{glibcrelease}
License: LGPL
Group:   Core/Runtime/Library	
Source0:	http://ftp.gnu.org/gnu/glibc/glibc-%{glibcversion}.tar.xz

Source2:	glibc_post_upgrade.c	
Source3:	hardlink.c
Source4:	build-locale-archive.c
Source5:    nsswitch.conf


Patch0:     glibc-fix-build_locale_archive.patch
Patch7:     glibc-sunrpc-rpcgen-cpp-path.patch
Patch9:     1055_all_glibc-resolv-dynamic.patch
Patch12:    0020_all_glibc-tweak-rfc1918-lookup.patch
Patch20:    1005_all_glibc-sigaction.patch
Patch21:    1070_all_glibc-fadvise64_64.patch
Patch22:    glibc-2.19-fix-build-locale-archive.patch

Provides: ldconfig
Provides: rtld(GNU_HASH)

%ifarch i386
%define nptl_target_cpu i486
%else
%define nptl_target_cpu %{_target_cpu}
%endif

%define _unpackaged_files_terminate_build 0


Requires(pre): basesystem

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

%package devel
Summary: Object files for development using standard C libraries.
Group:  Core/Development/Library 
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}, %{name} = %{version}-%{release}
Autoreq: true

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

%package headers
Summary: Header files for development using standard C libraries.
Group:  Core/Development/Library 
Provides: %{name}-headers(%{_target_cpu})
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
Autoreq: true

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

%package common
Group:  Core/Runtime/Library 
Summary: Common binaries and locale data for glibc
Autoreq: false
Requires: tzdata >= 2003a

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

#%package -n nscd
#Summary: A Name Service Caching Daemon (nscd).
#Group: System Environment/Daemons
#Conflicts: kernel < 2.2.0
#Requires: libselinux >= 1.17.10-1
#Conflicts: selinux-policy-targeted < 1.17.30-2.2
#Requires(pre): /sbin/chkconfig, /usr/sbin/useradd, /usr/sbin/userdel, sh-utils
#Autoreq: true
#
#%description -n nscd
#Nscd caches name service lookups and can dramatically improve
#performance with NIS+, and may help with DNS as well.

%package utils
Summary: Development utilities from GNU C library
Group:  Core/Runtime/Utility 
Requires: glibc = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%prep
%setup -q 
%patch0 -p1
%patch7 -p1
%patch9 -p1
%patch12 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

%build
GCC=gcc
GXX=g++
%ifarch %{ix86}
BuildFlags="-march=%{nptl_target_cpu} -mtune=generic"
%endif
%ifarch i686
BuildFlags="-march=i686 -mtune=generic"
%endif
%ifarch i386
BuildFlags="$BuildFlags -mno-tls-direct-seg-refs"
%endif
%ifarch x86_64
BuildFlags="-mtune=generic"
%endif

builddir=glibc-build

rm -rf $builddir
mkdir $builddir

mkdir everest
cp %{SOURCE3} everest
cp %{SOURCE4} everest
cd $builddir
EnableKernel="--enable-kernel=2.6.9"
BuildFlags="$BuildFlags -DNDEBUG=1 -fasynchronous-unwind-tables"
build_CFLAGS="$BuildFlags -g -O3 $*"

echo "libc_cv_forced_unwind=yes" >> config.cache
echo "libc_cv_c_cleanup=yes" >> config.cache
echo "libc_cv_x86_64_tls=yes" >> config.cache
echo "libc_cv_slibdir=/lib" >> config.cache
echo "slibdir=/lib" >> configparms
BUILD_CC="gcc" CFLAGS="$build_CFLAGS" ../configure --prefix=%{_prefix} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --disable-profile --enable-add-ons --with-tls --enable-kernel=2.6.0 --enable-obsolete-rpc --with-__thread --disable-werror --cache-file=config.cache

make -r CFLAGS="$build_CFLAGS" PARALLELMFLAGS=-s

%install
builddir=glibc-build

pushd glibc-build
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install_root=$RPM_BUILD_ROOT install
make install_root=$RPM_BUILD_ROOT localedata/install-locales
popd

install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/nsswitch.conf
## Don't include ld.so.cache
rm -f $RPM_BUILD_ROOT/etc/ld.so.cache

echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
touch $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
touch $RPM_BUILD_ROOT/etc/sysconfig/nscd

## Include %{_prefix}/%{_lib}/gconv/gconv-modules.cache
#> $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
#chmod 644 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/gconv/gconv-modules.cache
#

# Install the upgrade program
gcc -static -Os %{SOURCE2} -o $RPM_BUILD_ROOT/usr/sbin/glibc_post_upgrade -DNO_SIZE_OPTIMIZATION
 
#
strip -g $RPM_BUILD_ROOT%{_prefix}/%{_lib}/*.o

#
## Hardlink identical locale files together
gcc -O2 -o glibc-build/hardlink everest/hardlink.c
olddir=`pwd`
pushd ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/locale
rm locale-archive || :
# Intentionally we do not pass --alias-file=, aliases will be added
# by build-locale-archive.
$olddir/glibc-build/elf/ld.so \
  --library-path $olddir/glibc-build/ \
  $olddir/glibc-build/locale/localedef \
    --prefix ${RPM_BUILD_ROOT} --add-to-archive \
    *_*
rm -rf *_*
mv locale-archive{,.tmpl}
popd

#glibc-build/hardlink -vc $RPM_BUILD_ROOT%{_prefix}/lib/locale
#
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# BUILD THE FILE LIST
find $RPM_BUILD_ROOT -type f -or -type l |
	sed -e 's|.*/etc|%config &|' \
	    -e 's|.*/gconv/gconv-modules$|%verify(not md5 size mtime) %config(noreplace) &|' \
	    -e 's|.*/gconv/gconv-modules.cache|%verify(not md5 size mtime) &|' \
	    -e '/lib\/debug/d' > rpm.filelist.in
for n in %{_prefix}/share %{_prefix}/include %{_prefix}/%{_lib}/locale; do
    find ${RPM_BUILD_ROOT}${n} -type d | \
	grep -v '%{_prefix}/share$' | \
	grep -v '%{_infodir}' | \
	sed "s/^/%dir /" >> rpm.filelist.in
done

# primary filelist
SHARE_LANG='s|.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo|%lang(\1) &|'
LIB_LANG='s|.*/lib/locale/\([^/_]\+\)|%lang(\1) &|'
# rpm does not handle %lang() tagged files hardlinked together accross
# languages very well, temporarily disable
LIB_LANG=''
sed -e "s|$RPM_BUILD_ROOT||" -e "$LIB_LANG" -e "$SHARE_LANG" < rpm.filelist.in |
	grep -v '/etc/\(localtime\|nsswitch.conf\|ld.so.conf\|ld.so.cache\|default\)'  | \
	grep -v '/%{_lib}/lib\(pcprofile\|memusage\).so' | \
	grep -v 'bin/\(mtrace\|xtrace\|pcprofiledump\)' | \
	sort > rpm.filelist

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}
#mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_prefix}/%{_lib}
for i in $RPM_BUILD_ROOT%{_prefix}/bin/xtrace; do
  cp -a $i $i.tmp
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_prefix}/%{_lib}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_prefix}/%{_lib}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
    $i.tmp > $i
  chmod 755 $i; rm -f $i.tmp
done

#grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist
grep '%{_prefix}/include/gnu/stubs\.h' < rpm.filelist >> devel.filelist || :

grep '%{_prefix}/include' < rpm.filelist |
	egrep -v '%{_prefix}/include/(linuxthreads|gnu/stubs\.h|rpcsvc/rquota)' \
		> headers.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/%{_lib}/lib.*_p.a' rpm.filelist.full |
	egrep -v "(%{_prefix}/include)|(%{_infodir})" > rpm.filelist

grep '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_prefix}/%{_lib}/lib.*\.so' < rpm.filelist >> devel.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/%{_lib}/lib.*\.a' < rpm.filelist.full |
	grep -v '%{_prefix}/%{_lib}/.*\.o' |
	grep -v '%{_prefix}/%{_lib}/lib.*\.so'|
	grep -v '%{_prefix}/%{_lib}/linuxthreads' |
	grep -v 'nscd' > rpm.filelist

grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/%{_lib}/locale' < rpm.filelist | grep -v /locale-archive.tmpl >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
grep '%{_prefix}/share' < rpm.filelist \
  | grep -v '%{_prefix}/share/zoneinfo' >> common.filelist

mv rpm.filelist rpm.filelist.full
grep -v '%{_prefix}/bin' < rpm.filelist.full |
	grep -v '%{_prefix}/%{_lib}/locale' |
	grep -v '%{_prefix}/sbin/[^gi]' |
	grep -v '%{_prefix}/share' > rpm.filelist

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
echo '%{_prefix}/sbin/nscd' > nscd.filelist

cat > utils.filelist <<EOF
/%{_lib}/libmemusage.so
/%{_lib}/libpcprofile.so
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

#cjacker modified, use Asia/Shanghai as localtime
# /etc/localtime
#rm -f $RPM_BUILD_ROOT/etc/localtime
#cp -f $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo/Asia/Shanghai $RPM_BUILD_ROOT/etc/localtime
#ln -sf ..%{_prefix}/share/zoneinfo/US/Eastern $RPM_BUILD_ROOT/etc/localtime

cd everest
gcc -Os -static -o build-locale-archive build-locale-archive.c \
  ../glibc-build/locale/locarchive.o \
  ../glibc-build/locale/md5.o \
  -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
  -L../glibc-build
install -m 700 build-locale-archive $RPM_BUILD_ROOT/usr/sbin/build-locale-archive
cd ..



rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp
touch $RPM_BUILD_ROOT/etc/ld.so.conf
#touch -r timezone/northamerica $RPM_BUILD_ROOT/etc/localtime
#touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc
touch $RPM_BUILD_ROOT/etc/rpc

touch $RPM_BUILD_ROOT/%{_prefix}/%{_lib}/locale/locale-archive


#fix ldd PATH issue!!!!!
sed -i -e 's/lib64/lib/g' $RPM_BUILD_ROOT/%{_bindir}/ldd



%check
#pushd glibc-build
#make check
#popd

%post -p /usr/sbin/glibc_post_upgrade

%postun -p /sbin/ldconfig

%post common -p /usr/sbin/build-locale-archive

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
    rm -rf %{_prefix}/include/scsi
fi

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

#%clean
#rm -rf "$RPM_BUILD_ROOT"
#rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
#%verify(not md5 size mtime) %config(noreplace) /etc/localtime
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_prefix}/%{_lib}/gconv
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
#%doc README NEWS INSTALL FAQ BUGS NOTES PROJECTS CONFORMANCE
#%doc COPYING COPYING.LIB README.libm LICENSES
#%doc hesiod/README.hesiod
/usr/sbin/glibc_post_upgrade





%files -f common.filelist common
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/locale
%attr(0644,root,root) %{_prefix}/%{_lib}/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/locale/locale-archive
#%dir %attr(755,root,root) /etc/default
#%verify(not md5 size mtime) %config(noreplace) /etc/default/nss
#%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

%files -f utils.filelist utils
%defattr(-,root,root)

#%files -f nscd.filelist -n nscd
#%defattr(-,root,root)
##%config(noreplace) /etc/nscd.conf
##%config /etc/rc.d/init.d/nscd
#%dir %attr(0755,root,root) /var/run/nscd
#%dir %attr(0755,root,root) /var/db/nscd
#%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
#%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
#%ghost %config(missingok,noreplace) /etc/sysconfig/nscd


%changelog
