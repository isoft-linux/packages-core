Name:           libarchive
Version:        3.1.2 
Release:        3
Summary:        A library for handling streaming archive formats 

License:        BSD
URL:            http://www.libarchive.org/ 
Source0:        http://www.libarchive.org/downloads/libarchive-%{version}.tar.gz
# Disable -Werror
Patch0:         libarchive-2.7.0-disable-werror.patch

BuildRequires: bison
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: e2fsprogs-devel
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: openssl-devel

# The patch touches Makefile.am files:
BuildRequires: automake autoconf
BuildRequires: libtool

%description
Libarchive is a programming library that can create and read several different 
streaming archive formats, including most popular tar variants, several cpio 
formats, and both BSD and GNU ar variants. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure \
    --disable-static \
    --disable-bsdtar \
    --enable-bsdcpio \
    --without-nettle \
    --without-xml2
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name cpio.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name mtree.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name tar.5 -exec rm -f {} ';'


%check
make check

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Oct 23 2015 cjacker - 3.1.2-3
- Rebuild for new 4.0 release

