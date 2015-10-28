Name:           perl-YAML-Tiny
Version:        1.67
Release:        4%{?dist}
Summary:        Read/Write YAML files with as little code as possible
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/YAML-Tiny/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Fcntl)
Requires:       perl(Scalar::Util)

%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%setup -q -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING README
%{perl_vendorlib}/YAML/
%{_mandir}/man3/YAML::Tiny.3*

%changelog
* Fri Oct 23 2015 cjacker - 1.67-4
- Rebuild for new 4.0 release

