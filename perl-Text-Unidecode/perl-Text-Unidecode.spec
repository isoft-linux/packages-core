Name:           perl-Text-Unidecode
Version:        1.23
Release:        4%{?dist}
Summary:        US-ASCII transliterations of Unicode text
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Text-Unidecode/
Source0:        http://www.cpan.org/modules/by-module/Text/Text-Unidecode-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Runtime
BuildRequires:  perl(Exporter)
BuildRequires:  perl(integer)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests only
BuildRequires:  perl(Test)
BuildRequires:  perl(Text::Wrap)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description

Text::Unidecode provides a function, `unidecode(...)' that takes
Unicode data and tries to represent it in US-ASCII characters (i.e.,
the universally displayable characters between 0x00 and 0x7F). The
representation is almost always an attempt at *transliteration* -- i.e.,
conveying, in Roman letters, the pronunciation expressed by the text in
some other writing system.

%prep
%setup -q -n Text-Unidecode-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc README TODO.txt ChangeLog
%{perl_vendorlib}/Text/
%{_mandir}/man3/*.3*

%changelog
* Fri Oct 23 2015 cjacker - 1.23-4
- Rebuild for new 4.0 release

