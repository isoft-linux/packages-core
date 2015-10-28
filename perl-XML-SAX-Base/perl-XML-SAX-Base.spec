Name:           perl-XML-SAX-Base
Version:        1.08
Release:        8
Summary:        Base class SAX drivers and filters
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-SAX-Base/
Source0:        http://www.cpan.org/authors/id/G/GR/GRANTM/XML-SAX-Base-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More) >= 0.88
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Conflicts:      perl-XML-SAX < 0.99-1

%description
This module has a very simple task - to be a base class for Perl SAX drivers
and filters. It's default behaviour is to pass the input directly to the
output unchanged. It can be useful to use this module as a base class so
you don't have to, for example, implement the characters() callback.

%prep
%setup -q -n XML-SAX-Base-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;


mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/%{perl_vendorlib}/XML/SAX/BuildSAXBase.pl $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}

%check
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/*
%changelog
* Fri Oct 23 2015 cjacker - 1.08-8
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

