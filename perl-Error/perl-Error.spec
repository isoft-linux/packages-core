Name:           perl-Error
Version:        0.17022
Release:        2
Epoch:          1
Summary:        Error/exception handling in an OO-ish way
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Error/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Error-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Error package provides two interfaces. Firstly Error provides a
procedural interface to exception handling. Secondly Error is a base class
for errors/exceptions that can either be thrown, for subsequent catch, or
can simply be recorded.

%prep
%setup -q -n Error-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/Error.3pm.gz
%{_mandir}/man3/Error::Simple.3pm.gz

%changelog
* Fri Oct 23 2015 cjacker - 1:0.17022-2
- Rebuild for new 4.0 release

