Name:           perl-SGMLSpm
Version:        1.03ii
Release: 	    16.2
Summary:        Perl library for parsing the output of nsgmls

Group:          CoreDev/Runtime/Library/Perl
License:        GPL
URL:            http://search.cpan.org/dist/SGMLSpm/
Source0:    	http://www.cpan.org/authors/id/D/DM/DMEGG/SGMLSpm-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl >= 1:5.6.1
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       openjade

%description
Perl programs can use the SGMLSpm module to help convert SGML, HTML or XML
documents into new formats.


%prep
%setup -q -n SGMLSpm

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT{%{_bindir},%{perl_vendorlib}}
make install_system \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	PERL5DIR=$RPM_BUILD_ROOT%{perl_vendorlib}

%check

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/sgmlspl
%{perl_vendorlib}/SGMLS*
%{perl_vendorlib}/skel.pl


%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

