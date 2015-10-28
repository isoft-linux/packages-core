Name:           perl-Module-ScanDeps
Summary:        Recursively scan Perl code for dependencies
Version:        1.19
Release:        5%{?dist}
License:        GPL+ or Artistic
Source0:        http://search.cpan.org/CPAN/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Module-ScanDeps/
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
# Digest::MD5 is optional and not used by tests
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FileHandle)
# Getopt::Long not used by tests
BuildRequires:  perl(Module::Metadata)
# Storable is optional and not used by tests
# subs not used by tests
# Text::ParseWords not used by tests
BuildRequires:  perl(vars)
BuildRequires:  perl(version)
# VMS::Filespec never used
BuildRequires:  perl(warnings)
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(Encode)
Requires:       perl(File::Find)
Requires:       perl(Text::ParseWords)

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%prep
%setup -q -n Module-ScanDeps-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}

%check
#make test

%files
%doc AUTHORS Changes README
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
%{_mandir}/man3/Module::ScanDeps.3pm*

%changelog
* Fri Oct 23 2015 cjacker - 1.19-5
- Rebuild for new 4.0 release

