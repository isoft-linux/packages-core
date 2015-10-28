Name:           perl-XML-NamespaceSupport
Version:        1.09
Release:	2.2
Summary:        XML-NamespaceSupport Perl module

License:        GPL or Artistic
Url:            http://search.cpan.org/dist/XML-NamespaceSupport/
Source0:        http://www.cpan.org/authors/id/R/RB/RBERJON/XML-NamespaceSupport-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl >= 1:5.6.1
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.


%prep
%setup -q -n XML-NamespaceSupport-%{version}
chmod 644 Changes README *.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
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
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::NamespaceSupport.3pm.gz

%changelog
* Fri Oct 23 2015 cjacker - 1.09-2.2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

