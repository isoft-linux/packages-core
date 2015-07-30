#js need autoconf213
#we will not ship it in global system level
#just embeded autoconf213 here.

Summary:	JavaScript interpreter and libraries
Name:		js
Epoch:		1
Version:	1.8.5
Release:	14
License:	GPLv2+ or LGPLv2+ or MPLv1.1
Group:		Core/Runtime/Language
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/js185-1.0.0.tar.gz
Patch0:		js-1.8.5-64bit-big-endian.patch
Patch1:		js-1.8.5-secondary-jit.patch
Patch2:		js185-destdir.patch
Patch3:		js-1.8.5-537701.patch
Patch4:     js-isfinite.patch
Patch5:     js-fix-clang-build.patch

Source100: ftp://prep.ai.mit.edu/pub/gnu/autoconf/autoconf-2.13.tar.gz 
Patch100:     autoconf-2.12-race.patch
Patch101:     autoconf-2.13-mawk.patch
Patch102:     autoconf-2.13-notmp.patch
Patch103:     autoconf-2.13-c++exit.patch
Patch104:     autoconf-2.13-headers.patch
Patch105:     autoconf-2.13-autoscan.patch
Patch106:     autoconf-2.13-exit.patch
Patch107:     autoconf-2.13-wait3test.patch
Patch108:     autoconf-2.13-make-defs-62361.patch
Patch109:     autoconf-2.13-versioning.patch
Patch110:    autoconf213-destdir.patch

Provides:		libjs = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires:	nspr-devel >= 4.7
BuildRequires:	python
BuildRequires:  zip
BuildRequires:	ncurses-devel


%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
superset of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.


%package devel
Summary: Header files, libraries and development documentation for %{name}
Group:  Core/Development/Library
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: ncurses-devel readline-devel
Provides: libjs-devel = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}-%{version} -a100
%patch0 -p2 -b .64bit-big-endian
%patch1 -p2 -b .secondary-jit
%patch2 -p0 -b .destdir
%patch3 -p1 -b .537701
#%patch5 -p1
pushd js/src
%patch4 -p1
popd

pushd autoconf-2.13
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
popd


%build
pushd autoconf-2.13
./configure --prefix=`pwd`/../internal-autoconf --program-suffix=-2.13
make MAKEINFO=true 
make install MAKEINFO=true
popd

export PATH=`pwd`/internal-autoconf/bin:$PATH
cd js
# Rm parts with spurios licenses, binaries
# Some parts under BSD (but different suppliers): src/assembler
#rm -rf src/assembler src/yarr/yarr src/yarr/pcre src/yarr/wtf src/v8-dtoa
rm -rf src/ctypes/libffi src/t src/tests/src/jstests.jar src/tracevis src/v8

pushd src
autoconf-2.13
popd

# Create pkgconfig file
cat > libjs.pc << 'EOF'
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: libjs
Description: JS library
Requires: nspr >= 4.7
Version: %{version}
Libs: -L${libdir} -ljs
Cflags: -DXP_UNIX=1 -DJS_THREADSAFE=1 -I${includedir}/js
EOF


cd src
%configure \
    --with-system-nspr \
    --enable-threadsafe \
    --enable-readline
make %{?_smp_mflags}


%install
cd js
make -C src install DESTDIR=%{buildroot}
# We don't want this
rm -f %{buildroot}%{_bindir}/js-config
install -m 0755 src/jscpucfg src/shell/js \
       %{buildroot}%{_bindir}/
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

# For compatibility
# XXX do we really need libjs?!?!?!
pushd %{buildroot}%{_libdir}
ln -s libmozjs185.so.1.0 libmozjs.so.1
ln -s libmozjs185.so.1.0 libjs.so.1
ln -s libmozjs185.so libmozjs.so
ln -s libmozjs185.so libjs.so
popd

install -m 0644 libjs.pc %{buildroot}%{_libdir}/pkgconfig/

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc js/src/README.html
%{_bindir}/js
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/jscpucfg
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/js

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

