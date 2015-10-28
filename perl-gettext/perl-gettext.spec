Name:           perl-gettext
Version:        1.05
Release:        33%{?dist}
Summary:        Interface to gettext family of functions

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/gettext/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PV/PVANDRY/gettext-%{version}.tar.gz
Patch0:         http://patch-tracking.debian.net/patch/series/view/liblocale-gettext-perl/1.05-4/compatibility-with-POSIX-module.diff

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	gettext
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
# Encode is optional
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Obsoletes:	perl-Locale-gettext <= 1.05

%{?perl_default_filter}

%description
The gettext module permits access from perl to the gettext() family of 
functions for retrieving message strings from databases constructed to
internationalize software.

%prep
%setup -q -n gettext-%{version}
%patch0 -p1

%build
CC=gcc %{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" CC=gcc
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
unset LC_MESSAGES
case "$LANG" in
''|'C'|'POSIX' ) 
  export LANG=en_US.UTF-8;;
esac
make test


%files
%defattr(-,root,root,-)
%doc README
%{perl_vendorarch}/auto/Locale
%{perl_vendorarch}/Locale
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 23 2015 cjacker - 1.05-33
- Rebuild for new 4.0 release

