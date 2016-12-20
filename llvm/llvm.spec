#build as 'Release', otherwise delete this line.
%define debug_package %{nil}

#Release/RelWithDebInfo/Debug
%define build_type "Release"
%define llvm_targets "all"
%define llvm_default_target_triple "x86_64-isoft-linux"
%define clang_vendor "iSoft"

#check required a large amount of memory to run.
%global enable_check 0

#disable lldb build, lldb provided by swift(swift ship a modified version, swift REPL depend on it)
%define build_lldb 0

#for 3.9.0, lld/polly is disabled, it cause an issue about link
%define build_lld 0 
%define build_polly 0

%define build_libcxx 1
%define build_libcxxabi 1
%define build_libunwind 1
#libunwind shipped by llvm conflict with libunwind of GNU.
#we enable static build only.
#if disable libunwind build, libcxx Exception support will broken.
%define build_static_libunwind 1

%define build_openmp 1

%define build_test_suite 0

Name: llvm
Version: 3.9.0
Release: 8

Summary: Low Level Virtual Machine (LLVM) with clang	
License: University of Illinois/NCSA Open Source License 
URL: http://llvm.org

#note, libcxx/libcxxabi/libunwind/openmp is svn trunk 257014 
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

%if %{build_libcxx}
Source14: libcxx-%{version}.src.tar.xz
%endif

%if %{build_libcxxabi}
Source15: libcxxabi-%{version}.src.tar.xz
%endif

%if %{build_libunwind}
Source16: libunwind-%{version}.src.tar.xz
%endif

%if %{build_openmp}
Source17: openmp-%{version}.src.tar.xz
%endif

#polly wrapper scripts
Source20: pollycc
Source21: polly++

#emacs llvm-mode/tablegen-mode init file
Source30: llvm-init.el

#Add our own gcc tripplet to clang search path.
Patch0: clang-add-our-own-gcc-toolchain-tripplet-to-clang-path.patch

#We use 'lib' instead of 'lib64' under x86_64
#The intepretor of genenrated ELF by clang contains PATH.
#It's important.
Patch1: isoft-clang-lib64-to-lib.patch

#pp-trace in clang-tools-extra did not install properly.
Patch10: clang-extra-install-pp-trace.patch

Patch11: clang-fix-objc-exceptions-cflags.patch

# https://reviews.llvm.org/D24736
Patch12: msan-prevent-initialization-failure-with-newer-glibc.patch 

#configure build system of llvm latest svn already enable openmp support.
#this patch is for cmake build system
Patch20: llvm-enable-openmp-build.patch

# Warning on redeclaring with a conflicting asm label
# testcase: glibc v2.24.x
Patch21: warning-redeclaring-with-conflicting-asm-label.patch

# Static analyzer false positive of Unix API violation: Improper use of 'open', 
# when 'open' is in an alternative namespace
# testcase: k3b v17.04.0
Patch22: analyzer-false-positive-of-Unix-API-violation.patch

BuildRequires: clang gcc-go
BuildRequires: cmake >= 3.4.3
BuildRequires: ninja-build
BuildRequires: bison flex libtool-ltdl-devel
BuildRequires: zip bzip2 coreutils grep gzip sed unzip findutils
BuildRequires: chrpath
#not used, doc disabled.
BuildRequires: doxygen

BuildRequires: subversion

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

#if not build lld, remove older version.
%if %{build_lld}
Requires: alternatives
%else
Obsoletes: lld < %{version}-%{release}
Obsoletes: liblld-devel < %{version}-%{release}
Obsoletes: liblld-static < %{version}-%{release}
%endif

#if not build polly, remove older version.
%if %{build_polly}
BuildRequires: isl-devel >= 0.14
%else
Obsoletes: polly < %{version}-%{release}
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
Requires: ncurses-devel
Requires: zlib-devel

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
Requires: gmp-devel

%description -n polly
LLVM Framework for High-Level Loop and Data-Locality Optimizations

%package -n libpolly-devel
Summary: Header files for polly library.

%description -n libpolly-devel
This package contains header files for polly library.

%package -n libpolly-static
Summary: Static libraries for polly
Requires: libpolly-devel = %{version}-%{release}

%description -n libpolly-static
This package contains static libraries for develop program with polly library.
%endif
#end build_polly

#start of build_libcxx
%if %{build_libcxx}
%package -n libcxx
Summary: A standard conformant and high-performance implementation of the C++ Standard Library
Provides: libc++ = %{version}-%{release}
%if %{build_libcxxabi}
Provides: libcxxabi = %{version}-%{release}
%endif

#no matter build libcxxabi or not.
#these packages should be marked as obsoletes.
Obsoletes: libcxxabi < %{version}-%{release}

%description -n libcxx
The libc++ projects provide a standard conformant and high-performance implementation of the C++ Standard Library.

%package -n libcxx-devel
Summary: Headers and libraries for libcxx
Requires: libcxx = %{version}-%{release}
Provides: libc++-devel = %{version}-%{release}
%if %{build_libcxxabi}
Provides: libcxxabi-devel = %{version}-%{release}
%endif

#no matter build libcxxabi or not.
#these packages should be marked as obsoletes.
Obsoletes: libcxxabi-devel < %{version}-%{release}

%description -n libcxx-devel
Headers and libbraries for libcxx
%endif
#end build_libcxx

# start build_openmp
%if %{build_openmp}
%package -n openmp 
Summary: OpenMP runtime for use with the OpenMP implementation in Clang

%description -n openmp 
OpenMP runtime for use with the OpenMP implementation in Clang

%package -n openmp-devel
Summary: Headers and libraries for openmp.
Requires: openmp = %{version}-%{release}

%description -n openmp-devel
Headers and libraries for openmp.
%endif
# end build_openmp

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

%if %{build_libcxx}
mkdir -p projects/libcxx
tar xf %{SOURCE14} -C projects/libcxx --strip-components=1
%endif

%if %{build_libcxxabi}
mkdir -p projects/libcxxabi
tar xf %{SOURCE15} -C projects/libcxxabi --strip-components=1
%endif

%if %{build_libunwind}
mkdir -p projects/libunwind
tar xf %{SOURCE16} -C projects/libunwind --strip-components=1
%endif

%if %{build_openmp}
mkdir -p projects/openmp
tar xf %{SOURCE17} -C projects/openmp --strip-components=1
%endif


%patch0 -p1
%patch1 -p1
%patch10 -p1

%patch11 -p1

%patch12 -p0 -d projects/compiler-rt

%if %{build_openmp}
%patch20 -p1
%endif

%patch21 -p0 -d tools/clang
%patch22 -p0 -d tools/clang

%build
#we use clang/clang++ build llvm/clang
export CC="clang"
export CXX="clang++"

mkdir -p %{_target_platform}
pushd %{_target_platform}
#-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
cmake \
    -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE="%{build_type}" \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    -DLLVM_ENABLE_EH=ON \
    -DLLVM_ENABLE_FFI=ON \
    -DLLVM_ENABLE_RTTI=ON \
    -DFFI_INCLUDE_DIR:PATH="$(pkg-config --variable=includedir libffi)" \
    -DFFI_LIBRARY_DIR:PATH="$(pkg-config --variable=libdir libffi)" \
    -DLLVM_BINUTILS_INCDIR:PATH=%{_includedir} \
    -DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
    -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
    -DLLVM_TARGETS_TO_BUILD="%{llvm_targets}" \
%if %{build_libcxx}
    -DLIBCXX_ENABLE_ABI_LINKER_SCRIPT=ON \
%endif
%if %{build_libunwind}
%if %{build_static_libunwind}
    -DLIBUNWIND_ENABLE_SHARED=OFF \
%endif
    -DLIBCXXABI_USE_LLVM_UNWINDER=ON \
%else
    -DLIBCXXABI_USE_LLVM_UNWINDER=OFF \
%endif
    -DLLVM_DEFAULT_TARGET_TRIPLE="%{llvm_default_target_triple}" \
    -DCLANG_VENDOR="%{clang_vendor}" ..

ninja
popd

%install
rm -rf %{buildroot}

pushd %{_target_platform}
DESTDIR=%{buildroot} ninja install
popd


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

#vim files for .ll IR and .tb tablegen, no matter vim exist or not, we installed them.
mkdir -p %{buildroot}%{_datadir}/vim/vimfiles
cp -r utils/vim/ftdetect %{buildroot}%{_datadir}/vim/vimfiles
cp -r utils/vim/ftplugin %{buildroot}%{_datadir}/vim/vimfiles
cp -r utils/vim/indent %{buildroot}%{_datadir}/vim/vimfiles
cp -r utils/vim/syntax %{buildroot}%{_datadir}/vim/vimfiles

#emacs files for .ll IR and .tb tablegen
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 utils/emacs/llvm-mode.el %{buildroot}%{_datadir}/emacs/site-lisp
install -m 0644 utils/emacs/tablegen-mode.el %{buildroot}%{_datadir}/emacs/site-lisp
install -m 0644 %{SOURCE30} %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d

rm -rf %{buildroot}/usr/docs
rm -rf %{buildroot}%{_bindir}/c-index-test
rm -rf %{buildroot}%{_libdir}/LLVMHello.so
rm -rf %{buildroot}%{_datadir}/clang/*.applescript

#avoid conflict with libgomp provided by gcc
#Acctually clang only need libomp.so not libgomp.so
%if %{build_openmp}
rm -rf %{buildroot}%{_libdir}/libgomp.so
%endif

%if %{build_libunwind}
%if %{build_static_libunwind}
rm -rf %{buildroot}%{_libdir}/libunwind.a
%endif
%endif

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

%if %{build_libcxx}
%post -n libcxx -p /sbin/ldconfig
%postun -n libcxx -p /sbin/ldconfig
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
%{_bindir}/llvm-dwp
%{_bindir}/llvm-split
%{_bindir}/opt
%{_bindir}/llvm-c-test
%{_bindir}/llvm-lto
%{_bindir}/llvm-dsymutil
%{_bindir}/llvm-cxxdump
%{_bindir}/llvm-lib
%{_bindir}/llvm-pdbdump
%{_bindir}/obj2yaml
%{_bindir}/verify-uselistorder
%{_bindir}/yaml2obj
%{_bindir}/sancov
%{_bindir}/sanstats

#plugins.
%{_libdir}/BugpointPasses.so
%{_libdir}/libLTO.so
%{_libdir}/LLVMgold.so
%{_libdir}/bfd-plugins/LLVMgold.so

#vim files for .ll IR and .tb tablegen files.
#but not own dirs, it's belong to vim.
%{_datadir}/vim/vimfiles/*/*.vim

#emacs files for .ll IR and .tb tablegen files.
#but not own dirs, it's belong to vim.
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*.el


%files -n libllvm 
%defattr(-,root,root)
%{_libdir}/libLLVM*.so*

%files -n libllvm-devel
%defattr(-,root,root)
%{_bindir}/llvm-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_includedir}/%{name}-c
%{_includedir}/%{name}-c/*
%dir %{_libdir}/cmake/llvm
%{_libdir}/cmake/llvm/*
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

#it's belong to openmp
%if %{build_openmp}
%exclude %{_libdir}/clang/*/include/omp.h
%endif

%files -n clang-tools
%defattr(-,root, root,-)
%{_bindir}/clang-apply-replacements
%{_bindir}/clang-check
%{_bindir}/clang-format
%{_bindir}/modularize
%{_bindir}/clang-rename
%{_bindir}/clang-tidy
%{_bindir}/clang-query
%{_bindir}/git-clang-format
%{_bindir}/pp-trace
%{_bindir}/clang-include-fixer
%{_bindir}/find-all-symbols
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
%{_libexecdir}/c++-analyzer
%{_libexecdir}/ccc-analyzer

%{_mandir}/man1/*

%files -n libclang
%defattr(-,root,root)
%{_libdir}/libclang.so.3*

%files -n libclang-devel
%defattr(-,root,root)
%{_includedir}/clang
%{_includedir}/clang-c
%{_libdir}/libclang*.so
#actually, it's should not be here, it belong to clang-tools
%{_libdir}/libfindAllSymbols.a
%dir %{_libdir}/cmake/clang
%{_libdir}/cmake/clang/*


%files -n libclang-static
%defattr(-,root,root)
%{_libdir}/libclang*.a

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
%{_bindir}/ld.lld
%{_bindir}/lld-link

%files -n liblld-devel
%{_includedir}/lld

%files -n liblld-static
%{_libdir}/liblldCOFF.a
%{_libdir}/liblldCore.a
%{_libdir}/liblldDriver.a
%{_libdir}/liblldELF.a
%{_libdir}/liblldMachO.a
%{_libdir}/liblldReaderWriter.a
%{_libdir}/liblldYAML.a
%{_libdir}/liblldConfig.a
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

%files -n libpolly-static
%defattr(-,root,root)
%{_libdir}/libPolly*.a
%endif #end build_polly

#start build_libcxx
%if %{build_libcxx}
%files -n libcxx
%{_libdir}/libc++.so.*
%if %{build_libcxxabi}
%{_libdir}/libc++abi.so.*
%endif
%if %{build_libunwind}
%if !%{build_static_libunwind}
%{_libdir}/libunwind.so.*
%endif #build_static_libunwind
%endif #build_libunwind

%files -n libcxx-devel
%{_includedir}/c++/v1
%{_libdir}/libc++.so
%if %{build_libcxxabi}
%{_libdir}/libc++abi.so
%{_libdir}/libc++abi.a
%endif
%if %{build_libunwind}
%if !%{build_static_libunwind}
%{_libdir}/libunwind.so
%endif #build_static_libunwind
%endif #build_libunwind
%endif
#end build_libcxx

#start build_openmp
%files -n openmp 
%{_libdir}/libiomp5.so
%{_libdir}/libomp.so

%files -n openmp-devel
%{_libdir}/clang/*/include/omp.h
#end build_openmp

%changelog
* Tue Dec 20 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 3.9.0-8
- Static analyzer false positive of Unix API violation: Improper use of 'open', 
- when 'open' is in an alternative namespace
- testcase: scan-build (static analyzer) k3b v17.04.0

* Mon Dec 19 2016 Leslie Zhai <xiang.zhai@i-soft.com.cn> - 3.9.0-7
- Warning on redeclaring with a conflicting asm label
- testcase: scan-build (static analyzer) glibc v2.24.x

* Wed Nov 30 2016 sulit - 3.9.0-6
- recovery llvm-init.el, file-libs sometimes cause rpmbuild segmentation fault

* Mon Nov 21 2016 sulit <sulitsrc@gmail.com> - 3.9.0-5
- rebuild
- remove /usr/share/emacs/site-lisp/site-start.d/llvm-init.el, it cause rpmbuild
- segmentation fault.

* Fri Nov 18 2016 cjacker <cjacker@foxmail.com> - 3.9.0-4
- Disable lld/polly build by default, they cause an link issue in 3.9.0

* Fri Nov 18 2016 cjacker <cjacker@foxmail.com> - 3.9.0-3
- rebuild

* Thu Nov 17 2016 cjacker <cjacker@foxmail.com> - 3.9.0-2
- Update to 3.9.0

* Fri Aug 05 2016 sulit <sulitsrc@gmail.com> - 3.8.1-3
- uncomment gcc abi patch
- gcc abi tag support has a problem, we don't use it
- rollback

* Fri Aug 05 2016 sulit <sulitsrc@gmail.com> - 3.8.1-2
- compile llvm by clang

* Fri Jul 15 2016 sulit <sulitsrc@gmail.com> - 3.8.1-1
- upgrade llvm to official release version
- llvm 3.8.0 has a bug that don't build by gcc 6.1.0
- compile llvm by gcc

* Fri Jul 01 2016 sulit <sulitsrc@gmail.com> - 3.8.0-25
- update llvm to official release version 3.8.0


* Thu Jan 07 2016 Cjacker <cjacker@foxmail.com> - 3.7.1-24
- Update to 3.7.1 official release, codes unchanged

* Wed Dec 23 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-23
- Update libcxx/cxxabi/unwind/openmp to latest svn

* Fri Dec 18 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-22
- Update libcxx/libcxxabi/unwind/openmp and rebuild for beta4 release
- cfe/llvm/compiler-rt/clang-tools-extra keep unchanged

* Wed Dec 16 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-21
- Update libcxx/abi/unwind/openmp.
- cfe/llvm/compiler-rt/clang-tools-extra keeps untouched.

* Tue Dec 15 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-20
- Install IR and tablegen files for vim and emacs

* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-19
- Fix libllvm-devel requires

* Mon Dec 14 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-18
- Update, remove svn tag from release, it's should be rc2 now

* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-16.255420.svn
- Update to latest SVN rev of stable branch37

* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-13.252402.svn
- Enable libunwind static build, otherwise libcxx exception handler will failed

* Fri Dec 11 2015 Cjacker <cjacker@foxmail.com> - 3.7.1-12.252402.svn
- Add libcxx/libcxxabi/openmp/polly/lld

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
