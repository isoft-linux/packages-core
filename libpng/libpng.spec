Summary: A library of functions for manipulating PNG image format files
Name: libpng
Epoch: 2
Version: 1.6.17
Release: 4 
License: zlib
Group:  Core/Runtime/Library
URL: http://www.libpng.org/pub/png/
# Note: non-current tarballs get moved to the history/ subdirectory,
# so look there if you fail to retrieve the version you want
Source0: ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng16/libpng-%{version}.tar.xz

Patch0: libpng-%{version}-apng.patch.gz

BuildRequires: zlib-devel, pkgconfig, libtool
BuildRequires: autoconf >= 2.65
BuildRequires: automake

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group:  Core/Development/Library
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: zlib-devel%{?_isa} pkgconfig%{?_isa}

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%package static
Summary: Static PNG image format file library
Group:  Core/Development/Library
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of libpng.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary: Tools for PNG image format file library
Group:   Core/Runtime/Utility 
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
The libpng-tools package contains tools used by the authors of libpng.

%prep
%setup -q
%patch0 -p1


%build
autoreconf -vi

%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

# We don't ship .la files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

rpmclean
%check
#to run make check use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make check
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libpng16.so.*
%{_mandir}/man5/*

%files devel
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libpng*.so
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/libpng*.a

%files tools
%{_bindir}/pngfix

%changelog
