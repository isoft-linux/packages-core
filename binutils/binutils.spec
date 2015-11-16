%define ld_bfd_priority 50
%define ld_gold_priority 30

Name: binutils	
Version: 2.25.1
Release: 6 
Summary: A GNU collection of binary utilities	

License: MIT
Source0: ftp://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.bz2

#fix for gold exception_static_test/ifunc test failed 
#https://sourceware.org/bugzilla/show_bug.cgi?id=14675
#https://sourceware.org/bugzilla/show_bug.cgi?id=18521
Patch0: gold-test-failure-fix1.patch  
Patch1: gold-test-failure-fix2.patch  
Patch2: gold-test-failure-fix3.patch  
Patch3: gold-test-failure-fix4.patch  

#fix bfd.h header
Patch4: binutils-2.22.52.0.4-no-config-h-check.patch

Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

BuildRequires: texinfo, gettext, flex, bison, zlib-devel
#BuildRequires: /usr/bin/pod2man
BuildRequires: perl
BuildRequires: dejagnu, zlib-devel, glibc-devel, sharutils, bc
BuildRequires: libstdc++

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).


%package devel
Summary: BFD and opcodes static and dynamic libraries and header files

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a seperate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
../configure \
    --target=%{_target_platform} \
    --host=%{_target_platform} \
    --build=%{_target_platform} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-werror \
    --enable-shared \
    --enable-ld \
    --enable-gold \
    --enable-plugins \
    --disable-multilib \
    --enable-threads \
    --with-pic \
    --disable-gdb

make %{?_smp_mflags} MAKEINFO=true

# Do not use %%check as it is run after %%install where libbfd.so is rebuild
# with -fvisibility=hidden no longer being usable in its shared form.
echo ====================TESTING=========================
make -k check < /dev/null || :
echo ====================TESTING END=====================

popd

%install
pushd %{_target_platform}
make install DESTDIR=%{buildroot} MAKEINFO=true
# Rebuild libiberty.a with -fPIC.
# Future: Remove it together with its header file, projects should bundle it.
make -C libiberty clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

# Rebuild libbfd.a with -fPIC.
# Without the hidden visibility the 3rd party shared libraries would export
# the bfd non-stable ABI.
make -C bfd clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

# Rebuild libopcodes.a with -fPIC.
make -C opcodes clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes

install -m 644 bfd/libbfd.a %{buildroot}%{_libdir}
install -m 644 libiberty/libiberty.a %{buildroot}%{_libdir}
install -m 644 opcodes/libopcodes.a %{buildroot}%{_libdir}
popd

install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include

rm -rf $RPM_BUILD_ROOT%{_infodir}

##check
#pushd %{_target_platform} 
##this is all checkes.
#make check-binutils
#make check-gas
#make check-ld
#make check-gold
#popd

%post
%__rm -f %{_bindir}/ld
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.bfd %{ld_bfd_priority}
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.gold %{ld_gold_priority}
%{_sbindir}/alternatives --auto ld
/sbin/ldconfig
exit 0

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.bfd
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.gold
fi
exit 0

%files
%{_bindir}/*
%{_libdir}/libopcodes-*.so
%{_libdir}/libbfd-*.so
%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man1/*
%dir %{_prefix}/x86_64-isoft-linux
%{_prefix}/x86_64-isoft-linux/*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so

%changelog
* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 2.25.1-6
- Enable libbfd.a/libiberty.a/libopcodes.a

* Fri Oct 23 2015 cjacker - 2.25.1-5
- Rebuild for new 4.0 release

* Fri Sep 18 2015 Cjacker <cjacker@foxmail.com>
- refine build options.

* Sun Aug 09 2015 Cjacker <cjacker@foxmail.com>
- add patch4, remove config.h check from bfd.h

* Wed Jul 29 2015 Cjacker <cjacker@foxmail.com>
- add patch 0 to 3 to fix gold testfailed issues.
- now all checks should passed. 
