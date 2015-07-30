Name:           perl-libwww-perl
Version:        6.08
Release:        1
Summary:        A Perl interface to the World-Wide Web
Group:          Core/Runtime/Library/Perl
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/libwww-perl/
Source0:        libwww-perl-%{version}.tar.gz
BuildArch:      noarch

%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.

# RPM 4.8 style:
# Remove not-packaged features
%filter_from_requires /perl(Authen::NTLM)/d
%filter_from_requires /perl(HTTP::GHTTP)/d
# Remove underspecified dependencies
%filter_from_requires /^perl(Encode)\s*$/d
%filter_from_requires /^perl(File::Listing)\s*$/d
%filter_from_requires /^perl(HTTP::Date)\s*$/d
%filter_from_requires /^perl(HTTP::Negotiate)\s*$/d
%filter_from_requires /^perl(HTTP::Request)\s*$/d
%filter_from_requires /^perl(HTTP::Response)\s*$/d
%filter_from_requires /^perl(HTTP::Status)\s*$/d
%filter_from_requires /^perl(LWP::MediaTypes)\s*$/d
%filter_from_requires /^perl(MIME::Base64)\s*$/d
%filter_from_requires /^perl(Net::HTTP)\s*$/d
%filter_from_requires /^perl(URI)\s*$/d
%filter_from_requires /^perl(WWW::RobotRules)\s*$/d
%filter_setup

# RPM 4.9 style:
# Remove not-packaged features
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Authen::NTLM\\)
%global __requires_exclude %__requires_exclude|perl\\(HTTP::GHTTP\\)
# Remove underspecified dependencies
%global __requires_exclude %__requires_exclude|^perl\\(Encode\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(File::Listing\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Date\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Negotiate\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Request\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Response\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(HTTP::Status\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(LWP::MediaTypes\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(MIME::Base64\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(Net::HTTP\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(URI\\)\\s*$
%global __requires_exclude %__requires_exclude|^perl\\(WWW::RobotRules\)\\s*$

%prep
%setup -q -n libwww-perl-%{version} 

%build
# Install the aliases by default
%{__perl} Makefile.PL INSTALLDIRS=perl --aliases < /dev/null
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Some optional tests require resolvable hostname
#make test

%files
%defattr(-,root,root,-)
%doc AUTHORS Changes README*
%{_bindir}/*
%{perl_privlib}/lwp*.pod
%{perl_privlib}/LWP.pm
%{perl_privlib}/LWP/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*



%changelog
* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS
