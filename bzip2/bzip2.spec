Summary: A file compression utility
Name: bzip2
Version: 1.0.6
Release: 13
License: BSD
URL: http://www.bzip.org/
Source: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Patch0: bzip2-1.0.6-saneso.patch
Patch1: bzip2-1.0.6-cflags.patch
Patch2: bzip2-1.0.4-bzip2recover.patch

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary: Header files developing apps which will use bzip2
Requires: bzip2-libs = %{version}-%{release}

%description devel

Header files and a static library of bzip2 functions, for developing apps
which will use the library.

%package libs
Summary: Libraries for applications using bzip2

%description libs

Libraries for applications using the bzip2 compression format.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

make -f Makefile-libbz2_so AR=%{__ar} RANLIB=%{__ranlib} \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC" \
	%{?_smp_mflags} all

rm -f *.o
make AR=%{__ar} RANLIB=%{__ranlib} \
	CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64" \
	%{?_smp_mflags} all

%install
rm -rf ${RPM_BUILD_ROOT}

chmod 644 bzlib.h 
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir},%{_includedir}}
cp -p bzlib.h $RPM_BUILD_ROOT%{_includedir}
# temporary for rpm
install -m 644 libbz2.a $RPM_BUILD_ROOT%{_libdir}
install -m 755 libbz2.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install -m 755 bzip2-shared  $RPM_BUILD_ROOT%{_bindir}/bzip2
install -m 755 bzip2recover bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  $RPM_BUILD_ROOT%{_mandir}/man1/
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bunzip2
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bzcat
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
ln -s libbz2.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libbz2.so.1
ln -s libbz2.so.1 $RPM_BUILD_ROOT/%{_libdir}/libbz2.so
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzless.1

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig 

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%doc manual.html manual.pdf
%{_includedir}/*
%{_libdir}/*so
# Temporary for rpm
%{_libdir}/*.a

%changelog
* Fri Oct 23 2015 cjacker - 1.0.6-13
- Rebuild for new 4.0 release

