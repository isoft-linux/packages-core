Summary:	LZMA compression utilities
Name:		xz
Version:	5.2.1
Release:	1
License:	LGPLv2+
Group:	    Core/Runtime/Utility	
Source0:	http://tukaani.org/%{name}/%{name}-%{version}.tar.xz
URL:		http://tukaani.org/%{name}/
Requires:	%{name}-libs = %{version}-%{release}

#for xzdiff
Requires:   diffutils
#for xzdiff check
BuildRequires: diffutils

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.

%package 	libs
Summary:	Libraries for decoding LZMA compression
Group:      Core/Runtime/Library	
License:	LGPLv2+

%description 	libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package 	devel
Summary:	Devel libraries & headers for liblzma
Group:		Core/Development/Library
License:	LGPLv2+
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Devel libraries and headers for liblzma.

%package 	lzma-compat
Summary:	Older LZMA format compatibility binaries
Group:		Core/Runtime/Utility
License:	GPLv2+ and LGPLv2+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	lzma < %{version}
Provides:	lzma = %{version}

%description	lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.

%prep
%setup -q 

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/%{name}

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%clean
rm -rf %{buildroot}

%post libs 
/sbin/ldconfig %{_libdir}

%postun libs 
/sbin/ldconfig %{_libdir}

%files
%defattr(-,root,root,-)
%{_bindir}/*xz*
%{_mandir}/man1/*xz*

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.5*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%defattr(-,root,root,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*

%changelog
