Name:		perl-File-Remove
Version:	1.52
Release:	12%{?dist}
Summary:	Convenience module for removing files and directories
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/File-Remove/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/File-Remove-%{version}.tar.gz
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(ExtUtils::MM_Unix)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec) >= 3.29
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Test::More) >= 0.42
BuildArch:	noarch

%description
%{summary}

%prep
%setup -q -n File-Remove-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 1.52-12
- Rebuild for new 4.0 release

