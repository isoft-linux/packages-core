Name:           perl-URI
Version:        1.58
Release:        3%{?dist}
Summary:        A Perl module implementing URI parsing and manipulation

License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/URI/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/URI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).


%prep
%setup -q -n URI-%{version}
chmod 644 uri-test

%build
%{__perl} Makefile.PL INSTALLDIRS=perl
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README uri-test
%{perl_privlib}/URI*
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 23 2015 cjacker - 1.58-3
- Rebuild for new 4.0 release

* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS


