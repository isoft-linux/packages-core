Name:		perl-Unicode-EastAsianWidth
Version:	1.33
Release:	7%{?dist}
Summary:	East Asian Width properties
License:	CC0
URL:		http://search.cpan.org/dist/Unicode-EastAsianWidth/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AU/AUDREYT/Unicode-EastAsianWidth-%{version}.tar.gz
Patch0:		perl-Unicode-EastAsianWidth-no-inc.patch
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test)
#BuildRequires:	perl(Module::Package)
#BuildRequires:	perl(Pod::Markdown)
#BuildRequires:	perl(Module::Package::Au)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provide user-defined Unicode properties that deal with width
status of East Asian characters, as specified in
<http://www.unicode.org/unicode/reports/tr11/>.

%prep
%setup -q -n Unicode-EastAsianWidth-%{version}
#%patch0 -p1 -b .noinc
#rm -rf inc/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/Unicode/
%{_mandir}/man3/Unicode::EastAsianWidth.3pm*

%changelog
* Fri Oct 23 2015 cjacker - 1.33-7
- Rebuild for new 4.0 release

