%define ld_bfd_priority 50
%define ld_gold_priority 30

Name:		binutils	
Version:	2.25
Release:    2	
Summary:    A GNU collection of binary utilities	

Group:	    Core/Development/Utility	
License:	MIT
Source0:	%{name}-%{version}.tar.bz2

Patch0:     binutils-e9c1bdad.patch 
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

BuildRequires:  gcc, binutils	

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
Group:   Core/Development/Library

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
%build
mkdir -p build
pushd build
../configure --prefix=/usr \
	--disable-werror \
	--enable-shared \
    --enable-ld \
    --enable-gold \
    --enable-plugins \
	--disable-multilib \
    --enable-threads \
    --with-pic \
    --disable-gdb \
	--target=x86_64-pure64-linux \
	--host=x86_64-pure64-linux \
	--build=x86_64-pure64-linux

make %{?_smp_mflags} MAKEINFO=true
popd

%install
pushd build
make install DESTDIR=%{buildroot} MAKEINFO=true
popd

rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
pushd build
#gold exception_static_test will failed
#http://lists.gnu.org/archive/html//bug-binutils/2014-09/msg00025.html
make check MAKEINFO=true ||:
popd

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
%dir /usr/x86_64-pure64-linux
/usr/x86_64-pure64-linux/*

%files devel
%{_includedir}/*.h
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
