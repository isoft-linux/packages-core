#we never build gcj/ada
#up to 20150807, we had no plan to ship libgccjit

#control check log in package or not.
%global build_check_log 0 

#control build objc or not.
%global build_objc 0 

%ifarch %{ix86} x86_64 
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif

%ifarch %{ix86} x86_64
%global build_libasan 1
%else
%global build_libasan 0
%endif

%ifarch x86_64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif

%ifarch x86_64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif

%ifarch %{ix86} x86_64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif

%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif

%ifarch %{ix86} x86_64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif

%ifarch %{ix86} x86_64
%global build_libitm 1
%else
%global build_libitm 0
%endif

%ifarch %{ix86} x86_64
%global build_libmpx 1
%else
%global build_libmpx 0
%endif


%define gcc_version 6.1.0 
%define gcc_release 1
%define _unpackaged_files_terminate_build 0

%define gcc_target_platform %{_target_platform}

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}.1
License: GPLv3+ and GPLv2+ with exceptions
Source0: gcc-%{version}.tar.bz2

Patch0:  gcc-64bit-use-lib-as-libdir.patch
Patch1:  gcc-4.9-fix-cstddef-for-clang.patch 

URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: binutils >= 2.17.50.0.17-3
BuildRequires: mpc-devel >= 1.0.2 
BuildRequires: zlib-devel, gettext

%if %build_check_log
BuildRequires: autogen, dejagnu, expect, tcl
%endif

Requires: mpc >= 1.0.2 
Requires: binutils >= 2.17.50.0.17-3
Requires: libgcc = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}

Provides: gcc-c++ = %{version}-%{release}

AutoReq: true

%description
The gcc package contains the GNU Compiler Collection version 6.
You'll need this package in order to compile C code.


%package -n libgcc
Summary: GCC shared library
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libstdc++
Summary: GNU Standard C++ Library
Autoreq: true

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Requires: libstdc++ = %{version}-%{release}, %{_prefix}/%{_lib}/libstdc++.so.6
Autoreq: false 

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package go
Summary: go lang support for GCC
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Autoreq: true


%description go
This package adds go lang support to the GNU Compiler Collection.

%package -n libgo
Summary: go library
Autoreq: true

%description -n libgo
The libgo package contains a go library.

%package objc
Summary: Objective-C support for GCC
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Requires: gcc = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
Requires: libquadmath = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, mpc-devel >= 0.8.1
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Autoreq: true
Requires: libquadmath = %{version}-%{release}

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libquadmath
Summary: GCC Quad-Precision Math shared support library

%description -n libquadmath
This package contains GCC shared support library which is needed
for Quad-Precision Math support.

%package -n libitm
Summary: The GNU Transactional Memory library

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libatomic
Summary:  The GNU Atomic library

%description -n libatomic
This package contains the GNU Atomic library

%package -n libcilkrts
Summary: The Cilk runtime library

%description -n libcilkrts
This package contains the Cilk runtime library

%package -n libsanitizer
Summary: Various sanitizer runtime libraries

%description -n libsanitizer
This package contains various sanitizer libraries

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package gdb-plugin
Summary: GCC cc1 plugin for GDB
Requires: gcc = %{version}-%{release}

%description gdb-plugin
GCC cc1 plugin for GDB


#Up to now, we had no plan to ship it.
%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
Requires: libgccjit = %{version}-%{release}

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

#%package -n libvtv
#Summary: The virtual table verification library
#
#%description -n libvtv
#This package contains the virtual table verification library
#
#%package -n libssp
#Summary: The stack smashing protection library
#
#%description -n libssp
#This package contains the stack smashing protection library



%prep
%setup -q -n gcc-%{version}
%patch0 -p1
%patch1 -p1

echo 'iSoft %{version}-%{gcc_release}' > gcc/DEV-PHASE

# Do not run fixincludes
sed -i 's@\./fixinc\.sh@-c true@' gcc/Makefile.in

%build
mkdir build
pushd build
../configure \
    --target=%{gcc_target_platform} \
    --host=%{gcc_target_platform} \
    --build=%{gcc_target_platform} \
    --with-cpu=generic \
    --prefix=%{_prefix} \
    --enable-bootstrap \
    --enable-shared \
    --enable-threads=posix \
    --enable-checking=release \
%if %{build_objc}
    --enable-languages=c,c++,lto,go,fortran,objc,obj-c++ \
%else
    --enable-languages=c,c++,lto,go,fortran \
%endif
    --enable-plugin \
    --enable-initfini-array \
    --enable-gnu-unique-object \
    --enable-linker-build-id \
    --with-linker-hash-style=gnu \
    --enable-__cxa_atexit \
    --enable-gnu-indirect-function \
    --enable-c99 \
    --enable-long-long \
    --enable-libgomp \
    --enable-lto \
    --enable-libsanitizer \
%if %{build_libatomic}
    --enable-libatomic \
%endif
%if %{build_libquadmath}
    --enable-libquadmath \
%endif
%if %{build_libitm}
    --enable-libitm \
%endif
%if %{build_libcilkrts}
    --enable-libcilkrts \
%endif
%if %{build_libmpx}
    --enable-libmpx \
%endif
    --enable-symvers \
    --disable-libstdcxx-pch \
    --disable-multilib \
    --disable-libunwind-exceptions

make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
popd

%install
rm -fr $RPM_BUILD_ROOT

pushd build
make prefix=$RPM_BUILD_ROOT%{_prefix} install

%if %build_check_log
make check >gcc-%{version}-%{release}-check.log 2>&1 ||:
mkdir -p $RPM_BUILD_ROOT%{_docdir}/gcc
install -m0644 gcc-%{version}-%{release}-check.log $RPM_BUILD_ROOT%{_docdir}/gcc/gcc-%{version}-%{release}-check.log
%endif
popd


#create some useful links
#we use compiler-wrapper will switch between gcc/clang.
#ln -sf gcc $RPM_BUILD_ROOT%{_prefix}/bin/cc
rm -rf $RPM_BUILD_ROOT%{_prefix}/bin/c++

ln -sf gfortran %{buildroot}%{_prefix}/bin/f95

mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt


#remove files we do not ship.
rm -rf %{buildroot}/%{_bindir}/gcc-ar
rm -rf %{buildroot}/%{_bindir}/gcc-nm
rm -rf %{buildroot}/%{_bindir}/gcc-ranlib
rm -rf %{buildroot}%{_prefix}/%{_lib}/libssp* || :
rm -rf %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -rf %{buildroot}/%{_bindir}/%{gcc_target_platform}-gcc-ar
rm -rf %{buildroot}/%{_bindir}/%{gcc_target_platform}-gcc-nm
rm -rf %{buildroot}/%{_bindir}/%{gcc_target_platform}-gcc-ranlib
rm -rf %{buildroot}/%{_bindir}/%{gcc_target_platform}-gfortran
rm -rf %{buildroot}/%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools
rm -rf %{buildroot}/%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_version}/install-tools

#set up libstdc++ symbol for gdb
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/lib/
mv $RPM_BUILD_ROOT%{_libdir}/libstdc++.so.*.py $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/lib/

#fix lib perms.
chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so.*

# we do not ship info
rm -rf $RPM_BUILD_ROOT%{_infodir}

# do not ship gpl/gfdl/fsf-funding man page
rm -rf $RPM_BUILD_ROOT%{_mandir}/man7


find $RPM_BUILD_ROOT -name \*.la | xargs rm -f


%find_lang gcc
%find_lang cpplib
%find_lang libstdc++

cat cpplib.lang >>gcc.lang


%clean
rm -rf $RPM_BUILD_ROOT


%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig

%post -n libgomp -p /sbin/ldconfig
%postun -n libgomp -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig
%postun -n libgo -p /sbin/ldconfig

%if %{build_objc}
%post -n libobjc -p /sbin/ldconfig
%postun -n libobjc -p /sbin/ldconfig
%endif

%post -n libgfortran -p /sbin/ldconfig
%postun -n libgfortran -p /sbin/ldconfig

%post -n libsanitizer -p /sbin/ldconfig
%postun -n libsanitizer -p /sbin/ldconfig

%post gdb-plugin -p /sbin/ldconfig
%postun gdb-plugin -p /sbin/ldconfig

%if %{build_libquadmath}
%post -n libquadmath -p /sbin/ldconfig
%postun -n libquadmath -p /sbin/ldconfig
%endif

%if %{build_libatomic}
%post -n libatomic -p /sbin/ldconfig
%postun -n libatomic -p /sbin/ldconfig
%endif

%if %{build_libitm}
%post -n libitm -p /sbin/ldconfig
%postun -n libitm -p /sbin/ldconfig
%endif

%if %{build_libcilkrts}
%post -n libcilkrts -p /sbin/ldconfig
%postun -n libcilkrts -p /sbin/ldconfig
%endif

%if %{build_libmpx}
%post -n libmpx -p /sbin/ldconfig
%postun -n libmpx -p /sbin/ldconfig
%endif

#%post -n libvtv -p /sbin/ldconfig
#%postun -n libvtv -p /sbin/ldconfig
#
#%post -n libssp -p /sbin/ldconfig
#%postun -n libssp -p /sbin/ldconfig

%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi


%files -f gcc.lang
%defattr(-,root,root)
#%{_prefix}/bin/c++
%{_prefix}/bin/cpp
%{_prefix}/bin/g++
%{_prefix}/bin/gcc
#%{_prefix}/bin/cc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/%{gcc_target_platform}-c++
%{_prefix}/bin/%{gcc_target_platform}-g++
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{version}
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{gcc_target_platform}
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/*.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ssp
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/sanitizer

%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cilk
%endif

%dir %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/include-fixed/*

%dir %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include/*

%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/gtype.state

%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/gengtype

%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a

%{_mandir}/man1/cpp.1.gz
%{_mandir}/man1/g++.1.gz
%{_mandir}/man1/gcc.1.gz
%{_mandir}/man1/gcov.1.gz

%if %build_check_log
%{_docdir}/gcc/gcc-%{version}-%{release}-check.log
%endif

%files -n libgcc
%{_libdir}/libgcc_s.so
%{_libdir}/libgcc_s.so.1

%files -n libstdc++ -f libstdc++.lang
%{_libdir}/libstdc++.so.6
%{_libdir}/libstdc++.so.6.*

%files -n libstdc++-devel
%dir %{_includedir}/c++
%{_includedir}/c++/*
%{_libdir}/libstdc++.a
%{_libdir}/libstdc++fs.a
%{_libdir}/libstdc++.so
%{_libdir}/libsupc++.a
%dir %{_datadir}/gcc-*/python/libstdcxx
%{_datadir}/gcc-*/python/libstdcxx/*
%{_datadir}/gdb/auto-load/usr/lib/libstdc++.so.*.py*

%files -n libgomp 
%{_libdir}/libgomp.so.*
%{_libdir}/libgomp.a
%{_libdir}/libgomp.so
%{_libdir}/libgomp.spec
#%{_libdir}/libgomp-plugin-host_nonshm.so
#%{_libdir}/libgomp-plugin-host_nonshm.so.*


%files go
%defattr(-,root,root)
%ghost %{_prefix}/bin/go
%{_prefix}/bin/go.gcc
%ghost %{_prefix}/bin/gofmt
%{_prefix}/bin/gofmt.gcc
%{_bindir}/gccgo
%{_prefix}/bin/%{gcc_target_platform}-gccgo
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/go*
%{_mandir}/man1/gccgo*
%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_version}/cgo
%{_mandir}/man1/go.1.gz
%{_mandir}/man1/gofmt.1.gz

%files -n libgo
%defattr(-,root,root)
%{_libdir}/libgo.so.*
%{_libdir}/go/*
%{_libdir}/libgo.so
%{_libdir}/libgo.a
%{_libdir}/libnetgo.a
%{_libdir}/libgobegin.a
%{_libdir}/libgolibbegin.a

%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.*
%{_prefix}/%{_lib}/libgfortran.so
%{_prefix}/%{_lib}/libgfortran.a
%{_prefix}/%{_lib}/libgfortran.spec

%if %{build_objc}
%files objc
%defattr(-,root,root,-)
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc

%files objc++
%defattr(-,root,root,-)
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.a
%{_prefix}/%{_lib}/libobjc.so
%{_prefix}/%{_lib}/libobjc.so.*
%endif


%if %{build_libatomic}
%files -n libatomic
%{_libdir}/libatomic.so.*
%{_libdir}/libatomic.a
%{_libdir}/libatomic.so
%endif

%if %{build_libcilkrts}
%files -n libcilkrts
%{_libdir}/libcilkrts.so.*
%{_libdir}/libcilkrts.a
%{_libdir}/libcilkrts.so
%{_libdir}/libcilkrts.spec
%endif

%if %{build_libitm}
%files -n libitm
%{_libdir}/libitm.so.*
%{_libdir}/libitm.a
%{_libdir}/libitm.so
%{_libdir}/libitm.spec
%endif

%if %{build_libquadmath}
%files -n libquadmath
%{_libdir}/libquadmath.so.*
%{_libdir}/libquadmath.a
%{_libdir}/libquadmath.so
%endif

%if %{build_libmpx}
%files -n libmpx
%{_libdir}/libmpx.spec
%{_libdir}/libmpx.so.*
%{_libdir}/libmpx.a
%{_libdir}/libmpx.so
%{_libdir}/libmpxwrappers.a
%{_libdir}/libmpxwrappers.so
%{_libdir}/libmpxwrappers.so.*
%endif

%files -n libsanitizer
%defattr(-,root,root)
%{_libdir}/libsanitizer.spec
%if %{build_libtsan}
%{_prefix}/%{_lib}/libtsan.*
%endif
%if %{build_libasan}
%{_prefix}/%{_lib}/libasan*
%endif
%if %{build_liblsan}
%{_prefix}/%{_lib}/liblsan*
%endif
%if %{build_libubsan}
%{_prefix}/%{_lib}/libubsan*
%endif

%files gdb-plugin
%{_libdir}/libcc1.so
%{_libdir}/libcc1.so.*
%{_libdir}/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/libcc1plugin.so*

#%files -n libvtv
#%{_libdir}/libvtv.so.*
#%{_libdir}/libvtv.a
#%{_libdir}/libvtv.so
#
#%files -n libssp
#%defattr(-,root,root,-)
#%{_libdir}/libssp.a
#%{_libdir}/libssp.so
#%{_libdir}/libssp.so.0
#%{_libdir}/libssp.so.0.0.0
#%{_libdir}/libssp_nonshared.a


%changelog
* Fri Jun 24 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 6.1.0-1.1
- 6.1.0

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 5.3.0-12.2
- Update

* Fri Oct 23 2015 Cjacker <cjacker@foxmail.com> - 5.2.0-12.1
- Rebuild for new 4.0 release

* Fri Aug 07 2015 Cjacker <cjacker@foxmail.com>
- enable libmpx, libitm, libcilkrts
- remove libssp/vtv
- add macros to control whether to build a lot of libs or not.

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to 5.2.0
