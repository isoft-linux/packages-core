Summary:        SAX parser access API for Perl
Name:           perl-XML-SAX
Version:        0.99
Release:        9

Group:          CoreDev/Runtime/Library/Perl
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-SAX/
# Original source
# http://www.cpan.org/authors/id/G/GR/GRANTM/XML-SAX-%%{version}.tar.gz
Source0:        XML-SAX-%{version}-nopatents.tar.gz
# XML-SAX contains patented code that we cannot ship. Therefore we use
# this script to remove the patented code before shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./generate-tarball.sh %%{version}
Source1: generate-tarball.sh

# Fix rt#20126
Patch0:         perl-XML-SAX-0.99-rt20126.patch

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fatal)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test)
BuildRequires:  perl(XML::NamespaceSupport) >= 0.03
# XML::SAX::Base became independent package, BR just for test
BuildRequires:  perl(XML::SAX::Base)
BuildRequires:  perl(XML::SAX::Exception)
Requires:       perl(:MODULE_COMPAT_%(perl -MConfig -e 'print $Config{version}'))
Requires:       perl(LWP::UserAgent)

# Remove bogus XML::SAX::PurePerl* dependencies and unversioned provides
%global __requires_exclude ^perl\\(XML::SAX::PurePerl
%global __provides_exclude ^perl\\(XML::SAX::PurePerl\\)$

%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.


%prep
%setup -q -n XML-SAX-%{version}
%patch0 -p1

%build
echo N | %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

touch $RPM_BUILD_ROOT%{perl_vendorlib}/XML/SAX/ParserDetails.ini

%check
make test

# See http://rhn.redhat.com/errata/RHBA-2010-0008.html regarding these scriptlets
# perl-XML-LibXML-1.58-6 is in EL 5.8 and possibly later EL-5 releases
%post
if [ ! -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini" ] ; then
  perl -MXML::SAX -e \
    'XML::SAX->add_parser(q(XML::SAX::PurePerl))->save_parsers()' 2>/dev/null || :
else
  cp -p "%{perl_vendorlib}/XML/SAX/ParserDetails.ini" "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup"
fi

%triggerun -- perl-XML-LibXML < 1.58-8
if [ -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" ] ; then
  mv "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" "%{perl_vendorlib}/XML/SAX/ParserDetails.ini"
fi

%preun
# create backup of ParserDetails.ini, therefore user's configuration is used
if [ $1 -eq 0 ] ; then
  perl -MXML::SAX -e \
    'XML::SAX->remove_parser(q(XML::SAX::PurePerl))->save_parsers()' || :
fi
[ -f "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" ] && \
rm -rf "%{perl_vendorlib}/XML/SAX/ParserDetails.ini.backup" || :

%files
%dir %{perl_vendorlib}/XML/
%{perl_vendorlib}/XML/SAX.pm
%dir %{perl_vendorlib}/XML/SAX/
%{perl_vendorlib}/XML/SAX/*.pm
%doc %{perl_vendorlib}/XML/SAX/*.pod
%{perl_vendorlib}/XML/SAX/PurePerl/
%ghost %{perl_vendorlib}/XML/SAX/ParserDetails.ini
%{_mandir}/man3/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

