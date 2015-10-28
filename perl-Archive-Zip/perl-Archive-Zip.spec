Name:           perl-Archive-Zip
Version:        1.48
Release:        2%{?dist}
Summary:        Perl library for accessing Zip archives

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Archive-Zip/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/Archive-Zip-%{version}.tar.gz
BuildArch:      noarch
#https://rt.cpan.org/Public/Bug/Display.html?id=54827
Patch0:         Archive-Zip-cpan-rt-54827.patch
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
# Encode not used on Linux
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(integer)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Seekable)
# lib not used at tests
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(vars)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec::Unix)
# IO::Scalar not used
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)
BuildRequires:  unzip
BuildRequires:  zip
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Exporter)
Requires:       perl(File::Spec) >= 0.80

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(File::Spec\\)$

%description
The Archive::Zip module allows a Perl program to create, manipulate,
read, and write Zip archive files.
Zip archives can be created, or you can read from existing zip files.
Once created, they can be written to files, streams, or strings.
Members can be added, removed, extracted, replaced, rearranged, and
enumerated.  They can also be renamed or have their dates, comments,
or other attributes queried or modified.  Their data can be compressed
or uncompressed as needed.  Members can be created from members in
existing Zip files, or from existing directories, files, or strings.


%prep
%setup -q -n Archive-Zip-%{version}
%patch0 -p1
perl -MConfig -pi -e 's|^#!/usr/local/bin/perl|$Config{startperl}|' \
    examples/selfex.pl
for F in examples/*.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done


%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%files
%doc Changes examples/
%{_bindir}/crc32
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive*.3*


%changelog
* Fri Oct 23 2015 cjacker - 1.48-2
- Rebuild for new 4.0 release

