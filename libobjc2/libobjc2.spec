Summary: GNUstep Objective-C Runtime
Name: libobjc2 
Version: 1.7
Release: 1
Source: http://download.gna.org/gnustep/libobjc2-%{version}.tar.bz2
Patch0: libobjc-add-libdispatch-link.patch
Patch1: libobjc2-disable-toy-dispatch.patch
Group:  System Environment/Libraries 
License: see COPYING
BuildRequires: clang
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
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The libobjc2-devel package contains header files and documentation necessary
for developing programs using libobjc2.

%prep
%setup
%patch1 -p1
%build
#-rtlib=compiler-rt must be set when use -fnolibgcc
#since libobjc need __gcc_personality_v0 symbol
export CC=clang
export CXX=clang++
mkdir build
pushd build
cmake \
    -DCMAKE_C_FLAGS="-fPIC -D_DEFAULT_SOURCE" \
    -DCMAKE_CXX_FLAGS="-fPIC -stdlib=libc++ -D_DEFAULT_SOURCE" \
    -DDEFAULT_ENABLE_LLVM=ON \
    -DLIB_INSTALL_PATH=/usr/lib \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%attr(-,root,root) 
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%attr(-,root,root) 
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

