#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Cjacker comment:
#Never drop this spec and use others from other dists.
#Until you realy know how llvm/clang works as a toolchain and WHAT I AM DOING!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#link binaries and libraries to libcxx/libcxxabi
%global rebuild_use_libcxx 0 

#we had a try to drop libgcc/libstdc++ dependencies, and use libcxx/libcxxabi/libunwind as abi libraries.
#That means llvm/clang can be used without libgcc/libstdc++
#But not for production usage now, since it will break c++abi.
#But still keep it and maintain it here.
#By Cjacker

%global rebuild_drop_libgcc 0 


%global enable_rtti 1
%global enable_exception 1

#seems no enough memory to run all checks.
%global enable_check 0

#control components build.
%global build_lldb 1
#polly is good, but rarely used.
%global build_polly 0 
%global build_test_suite 0 
#lld does not works well now.
#also it need a static build LLVM
%global build_lld 1 

%define llvm_ver 3.6.2
%define cfe_ver 3.6.2
%define compiler_rt_ver 3.6.2
%define clang_tools_extra_ver 3.6.2
%define lld_ver 3.6.2
%define polly_ver 3.6.2
%define lldb_ver 3.6.2
%define test_suite_ver 3.6.2

Name:		llvm
Version:    3.6.2
Release:    6 
Summary:	Low Level Virtual Machine (LLVM) with clang	
License:   	University of llinois/NCSA Open Source License 
URL:        http://llvm.org
Group:		Core/Development/Utility
BuildRequires: clang

%if %{rebuild_use_libcxx}
BuildRequires: libcxx-devel
Requires:   libcxx
%endif

%if %{build_lldb}
BuildRequires:swig
%endif

%if %{build_polly}
BuildRequires: cloog-isl-shared-devel >= 0.18.1
%endif

BuildRequires: libedit-devel >= 3.0
BuildRequires: cmake, ninja-build
BuildRequires: chrpath
%if %{build_lld}
Requires: alternatives
%endif

Source:      llvm-%{llvm_ver}.src.tar.xz
Source1:	 cfe-%{cfe_ver}.src.tar.xz
Source2:     compiler-rt-%{compiler_rt_ver}.src.tar.xz
Source3:     clang-tools-extra-%{clang_tools_extra_ver}.src.tar.xz

Source10:    lldb-%{lldb_ver}.src.tar.xz
Source11:    polly-%{polly_ver}.src.tar.xz
Source12:    lld-%{lld_ver}.src.tar.xz
Source13:    test-suite-%{test_suite_ver}.src.tar.xz

Source20:    pollycc
Source21:    polly++

#cmake build system need this patch
#Patch0:      llvm-rtti-fix.patch

#if host clang use unwind instead of libgcc, this patch will be needed.
Patch1:       llvm-remove-ehtable-support-when-with-nolibgcc.patch

Patch10:      clang-pure64-gcc-toolchain.patch
Patch11:      clang-lib64-to-lib.patch
Patch12:      clang-fix-objc-exceptions-cflags.patch

#the dso link behaviour change can not load implicit DSO when link.
Patch13:      clang-add-c++abi-dso-when-stdlib-libc++.patch

#this patch add "-fnolibgcc" flag to clang to disable libgcc dependency
Patch14:      clang-use-unwind-with-fnolibgcc.patch

#pp-trace in clang-tools-extra did not install properly.
Patch15:      clang-extra-install-pp-trace.patch

%description
Low Level Virtual Machine (LLVM) is:
   1.A compilation strategy designed to enable effective program optimization across the entire lifetime of a program. LLVM supports effective optimization at compile time, link-time (particularly interprocedural), run-time and offline (i.e., after software is installed), while remaining transparent to developers and maintaining compatibility with existing build scripts.
   2.A virtual instruction set - LLVM is a low-level object code representation that uses simple RISC-like instructions, but provides rich, language-independent, type information and dataflow (SSA) information about operands. This combination enables sophisticated transformations on object code, while remaining light-weight enough to be attached to the executable. This combination is key to allowing link-time, run-time, and offline transformations.
   3.A compiler infrastructure - LLVM is also a collection of source code that implements the language and compilation strategy. The primary components of the LLVM infrastructure are a GCC-based C & C++ front-end, a link-time optimization framework with a growing set of global and interprocedural analyses and transformations, static back-ends for the X86, X86-64, PowerPC 32/64, ARM, Thumb, IA-64, Alpha, SPARC, MIPS and CellSPU architectures, a back-end which emits portable C code, and a Just-In-Time compiler for X86, X86-64, PowerPC 32/64 processors, and an emitter for MSIL.
   4.LLVM does not imply things that you would expect from a high-level virtual machine. It does not require garbage collection or run-time code generation (In fact, LLVM makes a great static compiler!). Note that optional LLVM components can be used to build high-level virtual machines and other systems that need these services.


%package -n libllvm
Summary:        LLVM shared libraries
Group:          Core/Runtime/Library 

%description -n libllvm
Shared libraries for the LLVM compiler infrastructure.


%package -n libllvm-devel
Summary:        Libraries and header files for LLVM
Group:          Core/Development/Library
Requires:       libllvm = %{version}-%{release}
Requires:       libffi-devel

%description -n libllvm-devel
This package contains library and header files needed to develop new
native programs that use the LLVM infrastructure.

%package -n libllvm-static
Summary:        Static libraries for LLVM
Group:          Core/Development/Library
Requires:       libllvm-devel = %{version}-%{release}

%description -n libllvm-static
This package contains static libraries needed to develop new
native programs that use the LLVM infrastructure.


%package -n clang 
Summary: A C language family frontend for LLVM
Group:   Core/Development/Language
Requires: llvm = %{version}-%{release} 
Requires: libllvm = %{version}-%{release} 
%if %{rebuild_use_libcxx}
Requires:   libcxx
Requires:   libcxx-devel
%endif

%description -n clang 
The goal of the Clang project is to create a new C, C++, Objective C and Objective C++ front-end for the LLVM compiler. 

%package -n clang-tools
Summary:  Extra tools of clang
Group:    Core/Development/Language
Requires: clang = %{version}-%{release}

%description -n clang-tools
Extra tools of clang.

%package -n libclang
Summary:        Libraries for develop program with libclang
Group:          Core/Runtime/Library
Requires:       libllvm = %{version}-%{release}

%description -n libclang
This package contains libraries for develop program with libclang.

%package -n libclang-devel
Summary:        Header files for clang
Group:          Core/Development/Library
Requires:       libclang = %{version}-%{release}

%description -n libclang-devel
This package contains header files for the Clang compiler.

%package -n libclang-static
Summary:        Static libraries for clang
Group:          Core/Development/Library
Requires:       libclang-devel = %{version}-%{release}

%description -n libclang-static
This package contains static libraries for develop program with Clang library.


%package -n lldb
Summary:        LLDB is a next generation, high-performance debugger 
Group:          Core/Development/Debugger
Requires:       liblldb = %{version}-%{release}

%description -n lldb 
LLDB is a next generation, high-performance debugger. It is built as a set of reusable components which highly leverage existing libraries in the larger LLVM Project, such as the Clang expression parser and LLVM disassembler.

%package -n liblldb
Summary:        Libraries for develop program with liblldb
Group:          Core/Runtime/Library 
Requires:       libllvm = %{version}-%{release}

%description -n liblldb
This package contains libraries for develop program with liblldb.

%package -n liblldb-devel
Summary:        Header files for lldb library. 
Group:          Core/Development/Library
Requires:       liblldb = %{version}-%{release}

%description -n liblldb-devel
This package contains header files for lldb library.

%package -n liblldb-static
Summary:        Static libraries for lldb
Group:          Core/Development/Library
Requires:       liblldb-devel = %{version}-%{release}

%description -n liblldb-static
This package contains static libraries for develop program with lldb library.


%package -n polly 
Summary:        LLVM Framework for High-Level Loop and Data-Locality Optimizations
Group:          Core/Development/Language
Requires:       clang = %{version}-%{release}
Requires:       cloog-isl >= 0.18.1
Requires:       gmp

%description -n polly 
LLVM Framework for High-Level Loop and Data-Locality Optimizations

%package -n libpolly-devel
Summary:        Header files for polly library.
Group:          Core/Development/Library

%description -n libpolly-devel
This package contains header files for polly library.

%package -n libpolly-static
Summary:        Static libraries for polly 
Group:          Core/Development/Library
Requires:       libpolly-devel = %{version}-%{release}

%description -n libpolly-static
This package contains static libraries for develop program with polly library.


%package -n lld
Summary:        The LLVM Linker
Group:          Core/Development/Language

%description -n lld
The LLVM Linker


%package -n liblld-devel
Summary:        Header files for lld library.
Group:          Core/Development/Library

%description -n liblld-devel
This package contains header files for lld library.

%package -n liblld-static
Summary:        Static libraries for lld
Group:          Core/Development/Library
Requires:       liblld-devel = %{version}-%{release}

%description -n liblld-static
This package contains static libraries for develop program with lld library.

%prep
if [ ! -d llvm-%{version}/vanilla ]; then
%setup -q -n llvm-%{version} -c
  mv llvm-%{version}.src vanilla
else
  cd llvm-%{version}
  if [ -d llvm-shared-%{version} ]; then
     rm -rf deleteme-shared-%{version}
     rm -rf deleteme-static-%{version}
     mv llvm-shared-%{version} deleteme-shared-%{version} 
     mv llvm-static-%{version} deleteme-static-%{version} 
     rm -rf deleteme-shared-%{version}
     rm -rf deleteme-static-%{version}
  fi
fi

cp -rl vanilla llvm-shared-%{version}
cp -rl vanilla llvm-static-%{version}

#shared build will only build llvm library, keep other things build as static linkage.
pushd llvm-static-%{version} 
mkdir -p tools/clang
mkdir -p tools/clang/tools/extra
mkdir -p projects/compiler-rt

tar xf %{SOURCE1} -C tools/clang --strip-components=1
tar xf %{SOURCE2} -C projects/compiler-rt --strip-components=1
tar xf %{SOURCE3} -C tools/clang/tools/extra --strip-components=1

%if %{build_lldb}
mkdir -p tools/lldb
tar xf %{SOURCE10} -C tools/lldb --strip-components=1
%endif

%if %{build_polly}
mkdir -p tools/polly
tar xf %{SOURCE11} -C tools/polly --strip-components=1
%endif

%if %{build_lld}
mkdir -p tools/lld
tar xf %{SOURCE12} -C tools/lld --strip-components=1
%endif

%if %{build_test_suite}
mkdir -p projects/test-suite
tar xf %{SOURCE13} -C projects/test-suite --strip-components=1
%endif

#%patch0 -p1
#register_frame is provided by libgcc
#if we use libc++/libc++abi/libunwind and remove libgcc support, it should be disabled.
%if %{rebuild_drop_libgcc}
%patch1 -p1
%endif

%patch10 -p1
%patch11 -p1

%patch12 -p1
%patch13 -p1

%patch14 -p1

%patch15 -p1
popd


#pushd llvm-shared-%{version}
#%patch0 -p1
#popd

%Build
#we use clang/clang++ build llvm/clang
export CC="clang"
export CXX="clang++"
mkdir -p llvm-shared-%{version}/build
mkdir -p llvm-static-%{version}/build

pushd llvm-static-%{version}/build 
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_COMPILER=clang++ \
    %if %{rebuild_use_libcxx}
    %if %{rebuild_drop_libgcc}
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -fnolibgcc -fPIC" \
    %else
    -DCMAKE_CXX_FLAGS="-std=c++11 -stdlib=libc++ -fPIC" \
    %endif #rebuild_drop_libgcc
    %else
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    %endif #rebuild_use_libcxx
    %if %{enable_exception}
    -DLLVM_ENABLE_EH=ON \
    %endif
    %if %{enable_rtti}
    -DLLVM_ENABLE_RTTI=ON \
    %endif
    -DBUILD_SHARED_LIBS=OFF \
    -DLLVM_ENABLE_PIC=ON \
    -DLLVM_TARGETS_TO_BUILD="all" \
    -DLLVM_DEFAULT_TARGET_TRIPLE="x86_64-pure64-linux" \
    -DCLANG_VENDOR="Pure64" ..
time ninja
popd


#shared library will never use libcxx.
pushd llvm-shared-%{version}/build
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_C_FLAGS="-fPIC" \
    -DCMAKE_CXX_FLAGS="-std=c++11 -fPIC" \
    %if %{enable_exception}
    -DLLVM_ENABLE_EH=ON \
    %endif
    %if %{enable_rtti}
    -DLLVM_ENABLE_RTTI=ON \
    %endif
    -DBUILD_SHARED_LIBS=ON \
    -DLLVM_ENABLE_PIC=ON \
    -DLLVM_TARGETS_TO_BUILD="all" \
    -DLLVM_DEFAULT_TARGET_TRIPLE="x86_64-pure64-linux" \
    -DCLANG_VENDOR="Pure64" ..
time ninja
popd

%install
rm -rf $RPM_BUILD_ROOT

pushd llvm-static-%{version}/build 
%if %{build_lldb}
  sed -i "s|set(CMAKE_INSTALL_PREFIX \"/usr\")|set(CMAKE_INSTALL_PREFIX \"$RPM_BUILD_ROOT/usr\")|" cmake_install.cmake
  sed -i "s|file(INSTALL DESTINATION \"/usr|file(INSTALL DESTINATION \"$RPM_BUILD_ROOT/usr|" tools/lldb/scripts/Python/modules/readline/cmake_install.cmake
  ninja install
%else
  DESTDIR=$RPM_BUILD_ROOT ninja install
%endif
popd

#yes, headers of shared build will replace static build. But It is OK!!!!!!!
pushd llvm-shared-%{version}/build
DESTDIR=$RPM_BUILD_ROOT ninja install
popd

#polly wrapper script
%if %{build_polly}
install -m0755 %{SOURCE20} $RPM_BUILD_ROOT/%{_bindir}/ 
install -m0755 %{SOURCE21} $RPM_BUILD_ROOT/%{_bindir}/ 
%endif

file %{buildroot}/%{_bindir}/* | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d
file %{buildroot}/%{_libdir}/*.so | awk -F: '$2~/ELF/{print $1}' | xargs -r chrpath -d


#it seems we need this
pushd $RPM_BUILD_ROOT/%{_bindir}
if [ ! -f llvm-ranlib ]; then
 ln -s llvm-ar llvm-ranlib
fi
popd

# Get rid of erroneously installed files.
#rm %{buildroot}%{_libdir}/*LLVMHello.*
#
#rm -rf $RPM_BUILD_ROOT/%{_libdir}/libgtest.so
#rm -rf $RPM_BUILD_ROOT/%{_libdir}/libgtest_main.so
#rm -rf $RPM_BUILD_ROOT/%{_libdir}/libgtest.a
#rm -rf $RPM_BUILD_ROOT/%{_libdir}/libgtest_main.a

rm -rf $RPM_BUILD_ROOT/usr/docs

rpmclean

%check
%if %{enable_check}
pushd llvm-static-%{version}/build
%if %{rebuild_use_libcxx}
echo "skip check"
%else
#Still had 115 cases failed.
echo "Check started, it will cause a lot of times to finish!"
ninja check-all ||:
%endif
popd

pushd llvm-shared-%{version}/build
%if %{rebuild_use_libcxx}
echo "skip check"
%else
echo "Check started, it will cause a lot of times to finish!"
ninja check-all ||:
%endif
popd
%endif #enable_check

%clean
#rm -rf $RPM_BUILD_ROOT

%post -n libllvm -p /sbin/ldconfig
%post -n libclang -p /sbin/ldconfig
%post -n liblldb -p /sbin/ldconfig


%postun -n libllvm -p /sbin/ldconfig
%postun -n libclang -p /sbin/ldconfig
%postun -n liblldb -p /sbin/ldconfig


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
%{_bindir}/macho-dump
%{_bindir}/opt
%{_bindir}/llvm-c-test
%{_bindir}/llvm-lto
%{_bindir}/llvm-dsymutil
%{_bindir}/llvm-vtabledump
%{_bindir}/obj2yaml
%{_bindir}/verify-uselistorder
%{_bindir}/yaml2obj

#these two so is not library but plugins.
%{_libdir}/BugpointPasses.so
%{_libdir}/libLTO.so

%files -n libllvm 
%defattr(-,root,root)
%{_libdir}/libLLVM*.so
%{_libdir}/*LLVMHello.*
%{_libdir}/libgtest*.so


%files -n libllvm-devel
%defattr(-,root,root)
%{_bindir}/llvm-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_includedir}/%{name}-c
%{_includedir}/%{name}-c/*
%dir %{_datadir}/llvm/cmake
%{_datadir}/llvm/cmake/*

%files -n libllvm-static 
%defattr(-,root,root)
%{_libdir}/libLLVM*.a
%{_libdir}/libgtest*.a

%files -n clang
%defattr(-,root,root)
%{_bindir}/clang
%{_bindir}/clang++
%{_bindir}/clang-check
%{_bindir}/clang-format
%{_bindir}/clang-3*
%{_bindir}/clang-cl
%{_bindir}/clang-rename
#%{_bindir}/clang-tblgen
%dir %{_libdir}/clang
%{_libdir}/clang/*

%files -n clang-tools
%defattr(-,root, root,-)
%{_bindir}/clang-apply-replacements
%{_bindir}/clang-modernize
%{_bindir}/clang-tidy
%{_bindir}/git-clang-format
#%{_libdir}/libmodernizeCore.so
%{_datadir}/clang/clang-format-bbedit.applescript
%{_datadir}/clang/clang-format-diff.py
%{_datadir}/clang/clang-format-sublime.py
%{_datadir}/clang/clang-format.el
%{_datadir}/clang/clang-format.py
%{_bindir}/pp-trace
%{_libdir}/libclangApplyReplacements.a
%{_libdir}/libclangQuery.a
%{_libdir}/libclangTidyGoogleModule.a
%{_libdir}/libclangTidy.a
%{_libdir}/libclangTidyLLVMModule.a
%{_libdir}/libmodernizeCore.a

%files -n libclang
%defattr(-,root,root)
%{_libdir}/libclang*.so
%{_libdir}/libclang.so.3*

%files -n libclang-devel
%defattr(-,root,root)
%{_includedir}/clang
%{_includedir}/clang-c

%files -n libclang-static
%defattr(-,root,root)
%{_libdir}/libclang*.a
#this files comes from clang-tools-extra
%exclude %{_libdir}/libclangApplyReplacements.a
%exclude %{_libdir}/libclangQuery.a
%exclude %{_libdir}/libclangTidyGoogleModule.a
%exclude %{_libdir}/libclangTidy.a
%exclude %{_libdir}/libclangTidyLLVMModule.a
%exclude %{_libdir}/libmodernizeCore.a

#start of build_lldb
%if %{build_lldb}
%files -n lldb 
%defattr(-,root,root)
%{python_sitearch}/lldb
%{python_sitearch}/readline.so
%{_bindir}/lldb*

%files -n liblldb
%defattr(-,root,root)
%{_libdir}/liblldb.so
%{_libdir}/liblldb.so.3*

%files -n liblldb-devel
%defattr(-,root,root)
%{_includedir}/lldb

%files -n liblldb-static
%defattr(-,root,root)
%{_libdir}/liblldb*.a
%endif 
#end of build_lldb


#start of build_polly
%if %{build_polly}
%files -n polly
%defattr(-,root,root)
%{_bindir}/pollycc
%{_bindir}/polly++
%{_libdir}/LLVMPolly.so

#%files -n libpolly-static
#%defattr(-,root,root)
#%{_libdir}/libpolly*.a

%files -n libpolly-devel
%defattr(-,root,root)
%{_includedir}/polly
%endif
#end of build_polly

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
%{_libdir}/liblldNative.a
%{_libdir}/liblldPECOFF.a
%{_libdir}/liblldPPCELFTarget.a
%{_libdir}/liblldPasses.a
%{_libdir}/liblldReaderWriter.a
%{_libdir}/liblldX86ELFTarget.a
%{_libdir}/liblldX86_64ELFTarget.a
%{_libdir}/liblldMipsELFTarget.a
%{_libdir}/liblldYAML.a
%{_libdir}/liblldAArch64ELFTarget.a
%{_libdir}/liblldConfig.a
%endif
#start of build_lld

%changelog
* Fri Jul 10 2015 cjacker <cjacker@foxmail.com>
- rebuild llvm, link to libstdc++/libgcc.
- add more comment in spec to explain why this spec is important! 
