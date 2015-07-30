Name: pcre
Version: 8.37
Release: 2
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
Patch0: pcre-01-seven-security-patches.patch
License: BSD
Group:  Core/Runtime/Library 
Prefix: %{_prefix}
Requires(pre): /sbin/ldconfig
BuildRequires: sed , libtool

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary: Development files for %{name}
Group: Core/Development/Library
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for %{name}.

%prep
%setup -q
%patch0 -p1
aclocal
libtoolize -if
automake --add-missing
autoconf
%build
%configure \
    --enable-jit \
    --enable-pcretest-libreadline \
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcre8 \
    --enable-pcre16 \
    --enable-pcre32 \
    --enable-pcregrep-libz \
    --enable-pcregrep-libbz2 
make %{?_smp_mflags}


%check
make check

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# get rid of unneeded *.la files
rm -f %{buildroot}%{_libdir}/*.la

rpmclean
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man3/*
%{_bindir}/pcre-config
%{_datadir}/doc
%changelog
