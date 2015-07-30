Name:           perl-Encode-Locale
Version:        1.02
Release:        3
Summary:        Determine the locale encoding
Group:          Core/Runtime/Library/Perl
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Encode-Locale/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Encode-Locale-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Encode) >= 2
BuildRequires:  perl(Encode::Alias)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Tests only:
BuildRequires:  perl(Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Multiline our @EXPORT_OK = qw( ... ) trips perl dep extractor
Requires:       perl(Encode) >= 2
Requires:       perl(Encode::Alias)
# Recommended:
Requires:       perl(I18N::Langinfo)

%description
In many applications it's wise to let Perl use Unicode for the strings
it processes.  Most of the interfaces Perl has to the outside world is
still byte based.  Programs therefore needs to decode byte strings
that enter the program from the outside and encode them again on the
way out.

%prep
%setup -q -n Encode-Locale-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor CC=clang
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Encode/
%{_mandir}/man3/Encode::Locale.3*

%changelog
