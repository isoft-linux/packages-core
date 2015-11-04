Summary: GNUstep Objective-C Runtime
Name: libobjc2 
Version: 1.8.1
Release: 2
URL: https://github.com/gnustep/libobjc2
License: see COPYING

Source: libobjc2-%{version}.tar.gz
Patch0: libobjc-add-libdispatch-link.patch
Patch1: libobjc2-disable-toy-dispatch.patch
#c++abi symbol is difference with stdc++
Patch2: libobjc2-fix-c++abi-diff-to-stdc++.patch
#weak should have a signature W.
Patch3: libobjc-property-should-have-W-with-Weak.patch

BuildRequires: clang llvm libllvm-devel libllvm-static libclang-devel libclang-static libcxx-devel libcxxabi-devel
Requires: clang

%description
The GNUstep Objective-C runtime is designed as a drop-in replacement for the
GCC runtime.  It supports both a legacy and a modern ABI, allowing code
compiled with old versions of GCC to be supported without requiring
recompilation.  The modern ABI adds the following features:

- Non-fragile instance variables.
- Protocol uniquing.
- Object planes support.
- Declared property introspection.

%package devel
Summary: Development tools for libobjc2
Requires: %{name} = %{version}-%{release}

%description devel
The libobjc2-devel package contains header files and documentation necessary
for developing programs using libobjc2.

%prep
%setup
#%patch1 -p1
#c++/c++abi diff with stdc++, if build with clang, we assume we use c++/c++abi.
%patch2 -p1
%patch3 -p1

%build
#-rtlib=compiler-rt must be set when use -fnolibgcc
#since libobjc need __gcc_personality_v0 symbol
mkdir build
pushd build
cmake \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_C_FLAGS="-fPIC -D_DEFAULT_SOURCE" \
    -DCMAKE_CXX_FLAGS="-fPIC -stdlib=libc++ -lc++abi -D_DEFAULT_SOURCE" \
    -DDEFAULT_ENABLE_LLVM=ON \
    -DLIB_INSTALL_PATH=%{_libdir} \
    -DBUILD_STATIC_LIBOBJC=ON \
    -DCMAKE_INSTALL_PREFIX=/usr ..
popd

%install
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd
pushd $RPM_BUILD_ROOT/usr/lib
ln -s libobjc.so.4.6 libobjc.so.4
ln -s libobjcxx.so.4.6 libobjcxx.so.4
popd

chmod 755 $RPM_BUILD_ROOT/usr/lib/*.so*

%check
#PropertyIntrospectionTest2 will failed, patch4 fixed it.
pushd build
make test
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%attr(-,root,root) 
%doc COPYING
%{_libdir}/*.so.*

%files devel
%attr(-,root,root) 
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%changelog
* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 1.8.1-2
- Update to 1.8.1

* Fri Oct 23 2015 cjacker - 1.8-2
- Rebuild for new 4.0 release

* Sat Jul 25 2015 Cjacker <cjacker@gmail.com>
- update to 1.8
- add patch3 to fix abi difference between c++/stdc++
- add patch4 to fix test.

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

