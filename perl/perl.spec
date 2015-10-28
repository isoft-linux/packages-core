%global __provides_exclude_from .*/auto/.*\\.so$|.*/%{perl_archlib}/.*\\.so$|%{_docdir}
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\(VMS|perl\\(Win32|perl\\(BSD::|perl\\(DB\\)
%global __requires_exclude perl\\(VMS|perl\\(BSD::|perl\\(Win32|perl\\(Tk|perl\\(Mac::|perl\\(Your::Module::Here|perl\\(FCGI|perl\\(Locale|perl\\(NDBM|perl\\(unicore::Name

%global perl_epoch      4

Name:	 	perl	
Version:	5.20.2
Release:	2
Epoch:      %{perl_epoch}
Summary:    Practical Extraction and Report Language	

License:	(GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
URL:		 http://www.perl.org
Source0:	%{name}-%{version}.tar.bz2

Patch0:     perl-5.20.2-gcc5_fixes-1.patch


BuildRequires:  zlib-devel, bzip2-devel
BuildRequires:  gcc, binutils	


# Compat provides
Provides: perl(:MODULE_COMPAT_5.16.2)
Provides: perl(:MODULE_COMPAT_5.16.1)
Provides: perl(:MODULE_COMPAT_5.16.0)
Provides: perl(:MODULE_COMPAT_5.20.0)
Provides: perl(:MODULE_COMPAT_5.20.2)

# Threading provides
Provides: perl(:WITH_ITHREADS)
Provides: perl(:WITH_THREADS)
# Largefile provides
Provides: perl(:WITH_LARGEFILES)
# PerlIO provides
Provides: perl(:WITH_PERLIO)

#/bin is a symbol link to /usr/bin, some package will require /bin/perl.
Provides: /bin/perl

%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting.  Perl is good at handling processes and files, and is especially
good at handling text.  Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.  A large
proportion of the CGI scripts on the web are written in Perl.  You need the
perl package installed on your system so that your system can handle Perl
scripts.


%package devel
Summary:        Header files for use in perl development
License:        GPL+ or Artistic
Requires:       perl = %{perl_epoch}:%{version}-%{release}

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%prep
%setup -q
%patch0 -p1
sed -i -e 's/less -R/less/g' ./Configure
sed -i -e 's/libswanted="\(.*\) nsl\(.*\)"/libswanted="\1\2"/g' ./Configure

%build
./Configure \
    -Dcccdlflags='-fPIC' \
    -Dccdlflags='-rdynamic' \
    -Doptimize="$RPM_OPT_FLAGS" \
    -Dprefix=/usr \
    -Dprivlib=/usr/share/perl5/core_perl \
    -Darchlib=/usr/lib/perl5/core_perl \
    -Dvendorprefix=/usr \
    -Dvendorlib=/usr/share/perl5/vendor_perl \
    -Dvendorarch=/usr/lib/perl5/vendor_perl \
    -Dsiteprefix=/usr/local \
    -Dsitelib=/usr/local/share/perl5/site_perl \
    -Dsitearch=/usr/local/lib/perl5/site_perl \
    -des \
    -Dusethreads \
    -Dcf_by='Pure64' \
    -Duselargefiles \
    -Dd_semctl_semun \
    -Duseshrplib \
    -Duseperlio \
    -Ud_csh \
    -Dusenm \
    -Dman1dir=/usr/share/man/man1 \
    -Dman3dir=/usr/share/man/man3 \
    -Dinstallman1dir=/usr/share/man/man1 \
    -Dinstallman3dir=/usr/share/man/man3 \
    -Dman1ext='1' \
    -Dman3ext='3pm'

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

    
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

find $RPM_BUILD_ROOT -type f -name '*.bs' -empty | xargs rm -f
rm -rf $RPM_BUILD_ROOT%{_libdir}/perl5/core_perl/.packlist

rm -rf $RPM_BUILD_ROOT/*.0

%files
%{_bindir}/*
%dir %{_libdir}/perl5
%{_libdir}/perl5/*
%{_datadir}/perl5/*
%exclude %{_bindir}/enc2xs
%exclude %dir %{_libdir}/perl5/*/Encode
%exclude %{_libdir}/perl5/*/Encode/*
%exclude %{_bindir}/h2xs
%exclude %{_bindir}/perlivp
%exclude %{_libdir}/perl5/core_perl/CORE/*.h
%{_mandir}/man1/*

%files devel
%{_bindir}/enc2xs
%dir %{_libdir}/perl5/*/Encode
%{_libdir}/perl5/*/Encode/*
%{_bindir}/h2xs
%{_bindir}/perlivp
%{_libdir}/perl5/core_perl/CORE/*.h
%{_mandir}/man3/*


%changelog
* Fri Oct 23 2015 cjacker - 4:5.20.2-2
- Rebuild for new 4.0 release

