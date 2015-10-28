Name:           perl-XML-Parser
Version:        2.41
Release:        10%{?dist}
Summary:        Perl module for parsing XML documents

License:        GPL+ or Artistic
Url:            http://search.cpan.org/dist/XML-Parser/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/XML-Parser-%{version}.tar.gz

BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  expat-devel
# The script LWPExternEnt.pl is loaded by Parser.pm
BuildRequires:  perl(LWP)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::file)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)


%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(XML::Parser\\)$

%description
This module provides ways to parse XML documents. It is built on top
of XML::Parser::Expat, which is a lower level interface to James
Clark's expat library. Each call to one of the parsing methods creates
a new instance of XML::Parser::Expat which is then used to parse the
document. Expat options may be provided when the XML::Parser object is
created. These options are then passed on to the Expat object on each
parse call. They can also be given as extra arguments to the parse
methods, in which case they override options given at XML::Parser
creation time.

%prep
%setup -q -n XML-Parser-%{version} 
chmod 644 samples/{canonical,xml*}
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' samples/{canonical,xml*}

%build
CC=gcc CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in samples/REC-xml-19980210.xml; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
  sed -i -e "s/encoding='ISO-8859-1'/encoding='UTF-8'/" "$file"
done

%check
make test

%files
%doc README Changes samples/
%{perl_vendorarch}/XML/
%{perl_vendorarch}/auto/XML/
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 23 2015 cjacker - 2.41-10
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

