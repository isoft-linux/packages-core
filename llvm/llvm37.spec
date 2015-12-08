#!!!!!!!!!!SVN!!!!!!!!!!
#checkout trunk: svn co http://llvm.org/svn/llvm-project/<component>/trunk <component>
#checkout branch: svn co http://llvm.org/svn/llvm-project/<component>/branches/release_XY <component>-XY.src 
#!!!!!!!!!!!!!!!!!!!!!!!

#build as 'Release', otherwise delete this line.
%define debug_package %{nil}

#Release/RelWithDebInfo/Debug
%define build_type "Release"
%define llvm_targets "all"
%define llvm_default_target_triple "x86_64-isoft-linux"
%define clang_vendor "iSoft"

#check required a large amount of memory to run.
%global enable_check 0

#build lldb or not. lldb provided by swift
%define build_lldb 0
%define build_lld 0
%define build_polly 0
%define build_test_suite 0

Name: llvm
Version: 3.7.1
Release: 6.252402.svn 

Summary: Low Level Virtual Machine (LLVM) with clang	
License: University of Illinois/NCSA Open Source License 
URL: http://llvm.org

#Essential components to construct minimal LLVM/Clang toolchain.
Source0: llvm-%{version}.src.tar.xz
Source1: cfe-%{version}.src.tar.xz
Source2: compiler-rt-%{version}.src.tar.xz
Source3: clang-tools-extra-%{version}.src.tar.xz

%if %{build_lldb}
Source10: lldb-%{version}.src.tar.xz
%endif

%if %{build_lld}
Source11: lld-%{version}.src.tar.xz
%endif

%if %{build_polly}
Source12: polly-%{version}.src.tar.xz
%endif

%if %{build_test_suite}
Source13: test-suite-%{version}.src.tar.xz
%endif

#polly wrapper scripts
Source20: pollycc
Source21: polly++

#Add our own gcc tripplet to clang search path.
Patch0: clang-add-our-own-gcc-toolchain-tripplet-to-clang-path.patch

#We use 'lib' instead of 'lib64' under x86_64
#The intepretor of genenrated ELF by clang contains PATH.
#It's important.
Patch1: clang-lib64-to-lib.patch
# Backport LLVM_LINK_LLVM_DYLIB option
Patch2: llvm-3.7.0-link-tools-against-libLLVM.patch
# https://llvm.org/bugs/show_bug.cgi?id=24157
Patch3: llvm-3.7.0-export-more-symbols.patch

#gcc abi_tag support
Patch4: 0001-add-gcc-abi_tag-support.patch
Patch5: 0002-Adapt-previous-Clang-trunk-patch-to-Clang-3.7.patch
Patch6: 0001-abi_tag-fix-segfault-when-build-libcxx.patch

# https://llvm.org/bugs/show_bug.cgi?id=24046
# Upstreamed - http://reviews.llvm.org/D13206
Patch7: clang-tools-extra-3.7.0-install-clang-query.patch 
# https://llvm.org/bugs/show_bug.cgi?id=24155
Patch8: 0001-New-MSan-mapping-layout-llvm-part.patch
Patch9: 0001-New-MSan-mapping-layout-compiler-rt-part.patch

Patch10: fix-broken-include-path.patch

#pp-trace in clang-tools-extra did not install properly.
Patch11: clang-extra-install-pp-trace.patch

Patch19: clang-fix-objc-exceptions-cflags.patch
#https://llvm.org/bugs/show_bug.cgi?id=25021
Patch20: add-test-hasSSE41-detection-pentium-dual-core.patch

# https://llvm.org/bugs/show_bug.cgi?id=24953
Patch30: lldb-3.7.0-avoid-linking-to-libLLVM.patch

BuildRequires: clang gcc-go
BuildRequires: cmake, ninja-build
BuildRequires: bison flex libtool-ltdl-devel
BuildRequires: zip bzip2 coreutils grep gzip sed unzip findutils
BuildRequires: chrpath
#not used, doc disabled.
BuildRequires: doxygen

#for test
BuildRequires: dejagnu tcl-devel

BuildRequires: glibc-devel
BuildRequires: glibc-headers
BuildRequires: libffi-devel
BuildRequires: libstdc++-devel
BuildRequires: python-devel
BuildRequires: libtirpc-devel
BuildRequires: valgrind-devel
BuildRequires: binutils-devel
BuildRequires: ncurses-devel
BuildRequires: libxml2-devel
BuildRequires: libedit-devel >= 3.0

%if %{build_lldb}
BuildRequires:swig
%endif

%if %{build_lld}
Requires: alternatives
%endif

%if %{build_polly}
BuildRequires: cloog-isl-shared-devel >= 0.18.1
%endif

%description
Low Level Virtual Machine (LLVM) is:
   1.A compilation strategy designed to enable effective program optimization across the entire lifetime of a program. LLVM supports effective optimization at compile time, link-time (particularly interprocedural), run-time and offline (i.e., after software is installed), while remaining transparent to developers and maintaining compatibility with existing build scripts.
   2.A virtual instruction set - LLVM is a low-level object code representation that uses simple RISC-like instructions, but provides rich, language-independent, type information and dataflow (SSA) information about operands. This combination enables sophisticated transformations on object code, while remaining light-weight enough to be attached to the executable. This combination is key to allowing link-time, run-time, and offline transformations.
   3.A compiler infrastructure - LLVM is also a collection of source code that implements the language and compilation strategy. The primary components of the LLVM infrastructure are a GCC-based C & C++ front-end, a link-time optimization framework with a growing set of global and interprocedural analyses and transformations, static back-ends for the X86, X86-64, PowerPC 32/64, ARM, Thumb, IA-64, Alpha, SPARC, MIPS and CellSPU architectures, a back-end which emits portable C code, and a Just-In-Time compiler for X86, X86-64, PowerPC 32/64 processors, and an emitter for MSIL.
   4.LLVM does not imply things that you would expect from a high-level virtual machine. It does not require garbage collection or run-time code generation (In fact, LLVM makes a great static compiler!). Note that optional LLVM components can be used to build high-level virtual machines and other systems that need these services.


%package -n libllvm
Summary: LLVM shared libraries

%description -n libllvm
Shared libraries for the LLVM compiler infrastructure.

%package -n libllvm-devel
Summary: Libraries and header files for LLVM
Requires: libllvm = %{version}-%{release}
Requires: libffi-devel

%description -n libllvm-devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.

%package -n libllvm-static
Summary: Static libraries for LLVM
Requires: libllvm-devel = %{version}-%{release}

%description -n libllvm-static
This package contains static libraries needed to develop new
native programs that use the LLVM infrastructure.

%package -n clang 
Summary: A C language family frontend for LLVM
Requires: llvm = %{version}-%{release} 
Requires: libllvm = %{version}-%{release} 

%description -n clang 
The goal of the Clang project is to create a new C, C++, Objective C and Objective C++ front-end for the LLVM compiler. 

%package -n clang-tools
Summary:  Extra tools of clang
Requires: clang = %{version}-%{release}

%description -n clang-tools
Extra tools of clang.

%package -n libclang
Summary: Libraries for develop program with libclang
Requires: libllvm = %{version}-%{release}

%description -n libclang
This package contains libraries for develop program with libclang.

%package -n libclang-devel
Summary: Header files for clang
Requires: libclang = %{version}-%{release}

%description -n libclang-devel
This package contains header files for the Clang compiler.

%package -n libclang-static
Summary: Static libraries for clang
Requires: libclang-devel = %{version}-%{release}

%description -n libclang-static
This package contains static libraries for develop program with Clang library.

# start of build_lldb
%if %{build_lldb}
%package -n lldb
Summary: LLDB is a next generation, high-performance debugger
Requires: liblldb = %{version}-%{release}

%description -n lldb
LLDB is a next generation, high-performance debugger. It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project, such as the Clang expression parser and LLVM disassembler.

%package -n liblldb
Summary: Libraries for develop program with liblldb
Requires: libllvm = %{version}-%{release}

%description -n liblldb
This package contains libraries for develop program with liblldb.

%package -n liblldb-devel
Summary: Header files for lldb library.
Requires: liblldb = %{version}-%{release}

%description -n liblldb-devel
This package contains header files for lldb library.

%package -n liblldb-static
Summary: Static libraries for lldb
Requires: liblldb-devel = %{version}-%{release}

%description -n liblldb-static
This package contains static libraries for develop program with lldb library.
%endif #end build_lldb

# start of build_lld
%if %{build_lld}
%package -n lld
Summary: The LLVM Linker

%description -n lld
The LLVM Linker


%package -n liblld-devel
Summary: Header files for lld library.

%description -n liblld-devel
This package contains header files for lld library.

%package -n liblld-static
Summary: Static libraries for lld
Requires: liblld-devel = %{version}-%{release}

%description -n liblld-static
This package contains static libraries for develop program with lld library.
%endif #end build_lld

#start of build_polly
%if %{build_polly}
%package -n polly
Summary: LLVM Framework for High-Level Loop and Data-Locality Optimizations
Requires: clang = %{version}-%{release}
Requires: cloog-isl >= 0.18.1
Requires: gmp-devel

%description -n polly
LLVM Framework for High-Level Loop and Data-Locality Optimizations

%package -n libpolly-devel
Summary: Header files for polly library.

%description -n libpolly-devel
This package contains header files for polly library.
%endif #end build_polly


%prep
%setup -q -n llvm-%{version}.src
mkdir -p tools/clang
mkdir -p projects/compiler-rt
mkdir -p tools/clang/tools/extra
tar xf %{SOURCE1} -C tools/clang --strip-components=1
tar xf %{SOURCE2} -C projects/compiler-rt --strip-components=1
tar xf %{SOURCE3} -C tools/clang/tools/extra --strip-components=1

%if %{build_lldb}
mkdir -p tools/lldb
tar xf %{SOURCE10} -C tools/lldb --strip-components=1

#always use python2, lldb python module only support python2 ABI now.
find tools/lldb -name Makefile -exec sed -i 's/python-config/python2-config/' {} +
sed -i 's|/usr/bin/env python|&2|' \
    tools/lldb/scripts/Python/{build-swig-Python,finish-swig-Python-LLDB}.sh
%endif

%if %{build_lld}
mkdir -p tools/lld
tar xf %{SOURCE11} -C tools/lld --strip-components=1
%endif

%if %{build_polly}
mkdir -p tools/polly
tar xf %{SOURCE12} -C tools/polly --strip-components=1
%endif

%if %{build_test_suite}
mkdir -p projects/test-suite
tar xf %{SOURCE13} -C projects/test-suite --strip-components=1
%endif


%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p2
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1 -d tools/clang/tools/extra
%patch8 -p1
%patch9 -p1 -d projects/compiler-rt
%patch10 -p1
%patch11 -p1

%patch19 -p1
%patch20 -p1

%if %{build_lldb}
%patch30 -p1 -d tools/lldb
%endif 

%build
#we use clang/clang++ build llvm/clang
export CC="clang"
export CXX="clang++"

mkdir -p %{_target_platform}
pushd %{_target_platform}
cmake \
    -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DCMAKE_BUILD_TYPE="%{build_type}" \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    -DLLVM_ENABLE_EH=ON \
    -DLLVM_ENABLE_RTTI=ON \
    -DLLVM_BINUTILS_INCDIR:PATH=/usr/include \
    -DFFI_INCLUDE_DIR:PATH="$(pkg-config --variable=includedir libffi)" \
    -DFFI_LIBRARY_DIR:PATH="$(pkg-config --variable=libdir libffi)" \
    -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
    -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
    -DLLVM_DYLIB_EXPORT_ALL=ON \
    -DLLVM_TARGETS_TO_BUILD="%{llvm_targets}" \
    -DLLVM_DEFAULT_TARGET_TRIPLE="%{llvm_default_target_triple}" \
    -DCLANG_VENDOR="%{clang_vendor}" ..
ninja
popd

%install
rm -rf %{buildroot}

pushd %{_target_platform}
DESTDIR=%{buildroot} ninja install
popd

#install clang-analyzer
pushd tools/clang
mkdir -p %{buildroot}%{_datadir}
for TOOL in scan-{build,view}; do
    cp -a tools/$TOOL %{buildroot}%{_datadir}/
    ln -s %{_datadir}/$TOOL/$TOOL %{buildroot}%{_bindir}/$TOOL
done

# man page
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{_datadir}/scan-build/scan-build.1 %{buildroot}%{_mandir}/man1/

# scan-build looks for clang within the same directory
ln -sf %{_bindir}/clang %{buildroot}%{_datadir}/scan-build/clang
popd # end clang-analyzer installation


# Symlink LLVMgold.so to /usr/lib/bfd-plugins
# Bug:
# sudo alternatives --set ld /usr/bin/ld.gold
# echo 'main(){b(1);}' > a.c
# echo 'b(int a){printf("%d\\n");}' > b.c
# clang -flto b.c -c
# clang -flto a.c -c
# ar q b.a b.o
# ranlib b.a
# clang -flto a.o b.a
mkdir -p %{buildroot}%{_libdir}/bfd-plugins
ln -sf ../LLVMgold.so %{buildroot}%{_libdir}/bfd-plugins/LLVMgold.so

#remove rpath.
file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d

#it seems we need this
pushd %{buildroot}/%{_bindir}
if [ ! -f llvm-ranlib ]; then
 ln -s llvm-ar llvm-ranlib
fi
popd

#polly wrapper script
%if %{build_polly}
install -m0755 %{SOURCE20} $RPM_BUILD_ROOT/%{_bindir}/
install -m0755 %{SOURCE21} $RPM_BUILD_ROOT/%{_bindir}/
%endif

rm -rf %{buildroot}/usr/docs
rm -rf %{buildroot}%{_bindir}/c-index-test
rm -rf %{buildroot}%{_libdir}/LLVMHello.so
rm -rf %{buildroot}%{_datadir}/clang/*.applescript

%check
%if %{enable_check}
pushd %{_target_platform}
ninja check-all ||:
popd
%endif

%post -n libllvm -p /sbin/ldconfig
%post -n libclang -p /sbin/ldconfig

%postun -n libllvm -p /sbin/ldconfig
%postun -n libclang -p /sbin/ldconfig

%if %{build_lldb}
%post -n liblldb -p /sbin/ldconfig
%postun -n liblldb -p /sbin/ldconfig
%endif

%if %{build_lld}
%post -n lld
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/lld 30

%preun -n lld
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ld %{_bindir}/lld
fi
exit 0
%endif

%files
%defattr(-,root,root)
%{_bindir}/bugpoint
%{_bindir}/llc
%{_bindir}/lli
%{_bindir}/llvm-ar
%{_bindir}/llvm-as
%{_bindir}/llvm-bcanalyzer
%{_bindir}/llvm-cov
%{_bindir}/llvm-diff
%{_bindir}/llvm-dis
%{_bindir}/llvm-dwarfdump
%{_bindir}/llvm-extract
%{_bindir}/llvm-link
%{_bindir}/llvm-mc
%{_bindir}/llvm-mcmarkup
%{_bindir}/llvm-nm
%{_bindir}/llvm-objdump
%{_bindir}/llvm-ranlib
%{_bindir}/llvm-readobj
%{_bindir}/llvm-rtdyld
%{_bindir}/llvm-size
%{_bindir}/llvm-stress
%{_bindir}/llvm-symbolizer
%{_bindir}/llvm-tblgen
%{_bindir}/llvm-profdata
%{_bindir}/opt
%{_bindir}/llvm-c-test
%{_bindir}/llvm-lto
%{_bindir}/llvm-dsymutil
%{_bindir}/llvm-cxxdump
%{_bindir}/llvm-lib
%{_bindir}/llvm-pdbdump
%{_bindir}/macho-dump
%{_bindir}/obj2yaml
%{_bindir}/verify-uselistorder
%{_bindir}/yaml2obj
#plugins.
%{_libdir}/BugpointPasses.so
%{_libdir}/libLTO.so
%{_libdir}/LLVMgold.so
%{_libdir}/bfd-plugins/LLVMgold.so

%files -n libllvm 
%defattr(-,root,root)
%{_libdir}/libLTO.so.*
%{_libdir}/libLLVM*.so*

%files -n libllvm-devel
%defattr(-,root,root)
%{_bindir}/llvm-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_includedir}/%{name}-c
%{_includedir}/%{name}-c/*
%dir %{_datadir}/llvm/cmake
%{_datadir}/llvm/cmake/*
%{_libdir}/libLLVM*.so

%files -n libllvm-static
%defattr(-,root,root)
%{_libdir}/libLLVM*.a

%files -n clang
%defattr(-,root,root)
%{_bindir}/clang
%{_bindir}/clang++
%{_bindir}/clang-3*
%{_bindir}/clang-cl
%dir %{_libdir}/clang
%{_libdir}/clang/*

%files -n clang-tools
%defattr(-,root, root,-)
%{_bindir}/clang-apply-replacements
%{_bindir}/clang-check
%{_bindir}/clang-format
%{_bindir}/clang-modernize
%{_bindir}/clang-rename
%{_bindir}/clang-tidy
%{_bindir}/clang-query
%{_bindir}/git-clang-format
%{_bindir}/pp-trace
%dir %{_datadir}/clang/
%{_datadir}/clang/*.py*
%{_datadir}/clang/*.el

#clang analyzer
%{_bindir}/scan-build
%{_bindir}/scan-view
%dir %{_datadir}/scan-build
%{_datadir}/scan-build/*
%dir %{_datadir}/scan-view
%{_datadir}/scan-view/*
%{_mandir}/man1/*

%files -n libclang
%defattr(-,root,root)
%{_libdir}/libclang.so.3*

%files -n libclang-devel
%defattr(-,root,root)
%{_includedir}/clang
%{_includedir}/clang-c
%{_libdir}/libclang*.so

%files -n libclang-static
%defattr(-,root,root)
%{_libdir}/libclang*.a
%{_libdir}/libmodernizeCore.a

#start of build_lldb
%if %{build_lldb}
%files -n lldb
%defattr(-,root,root)
%{_bindir}/lldb*
%{_bindir}/*argdumper
%{python_sitearch}/lldb
%{python_sitearch}/readline.so

%files -n liblldb
%defattr(-,root,root)
#python module need it.
#so it's not in devel package but here.
%{_libdir}/liblldb.so
%{_libdir}/liblldb.so.3*

%files -n liblldb-devel
%defattr(-,root,root)
%{_includedir}/lldb

%files -n liblldb-static
%defattr(-,root,root)
%{_libdir}/liblldb*.a
%endif #end build_lldb

#start of build_lld
%if %{build_lld}
%files -n lld
%{_bindir}/lld

%files -n liblld-devel
%{_includedir}/lld

%files -n liblld-static
%{_libdir}/liblldCore.a
%{_libdir}/liblldDriver.a
%{_libdir}/liblldELF.a
%{_libdir}/liblldHexagonELFTarget.a
%{_libdir}/liblldMachO.a
%{_libdir}/liblldPECOFF.a
%{_libdir}/liblldReaderWriter.a
%{_libdir}/liblldX86ELFTarget.a
%{_libdir}/liblldX86_64ELFTarget.a
%{_libdir}/liblldMipsELFTarget.a
%{_libdir}/liblldYAML.a
%{_libdir}/liblldAArch64ELFTarget.a
%{_libdir}/liblldConfig.a
%{_libdir}/liblldARMELFTarget.a
%{_libdir}/liblldCOFF.a
%{_libdir}/liblldExampleSubTarget.a
%endif #end build_lld

#start of polly
%if %{build_polly}
%files -n polly
%defattr(-,root,root)
%{_bindir}/pollycc
%{_bindir}/polly++
%{_libdir}/LLVMPolly.so

%files -n libpolly-devel
%defattr(-,root,root)
%{_includedir}/polly
%endif #end build_polly



%changelog
* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-6.252402.svn
- Clean spec, disable lld/lldb completely.
- Use LLVM_BUILD_LLVM_DYLIB to build shared library.
- Add gcc abi_tag patches(#4,#5,#6)

* Fri Dec 04 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-5.252402.svn
- Disable lldb/lld packages.
- lldb provided by swift because it's need a modified lldb.
- lld is rarely used.

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-4.252402.svn
- Update to svn 252402

* Mon Oct 26 2015 cjacker - 3.7.1-3.svn20151017
- Update to 3.7.1 svn 251274
- Add patch20 to fix cpu type detect issue. this issue will cause mesa not work on old core2 CPU.

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.1svn

* Wed Sep 02 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.0

* Tue Aug 11 2015 Cjacker <cjacker@foxmail.com>
- update to 3.7.0svn
- bump version to 3.7.0, wait for release.

* Sat Jul 25 2015 Cjacker <cjacker@foxmail.com>
- first build of 3.7.0rc1

* Fri Jul 10 2015 Cjacker <cjacker@foxmail.com>
- rebuild llvm, link to libstdc++/libgcc.
- add more comment in spec to explain why this spec is important! 