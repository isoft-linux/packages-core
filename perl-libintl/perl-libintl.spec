Summary: Internationalization library for Perl, compatible with gettext
Name: perl-libintl
Version: 1.20
Release: 16%{?dist}
License: LGPLv2+
Group: Development/Libraries
URL: http://search.cpan.org/dist/libintl-perl/
Source: http://search.cpan.org/CPAN/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides: perl-libintl-perl = %{version}-%{release}
BuildRequires: perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(constant)
BuildRequires: perl(Cwd)
BuildRequires: perl(Encode)
BuildRequires: perl(Encode::Alias)
BuildRequires: perl(Exporter)
BuildRequires: perl(IO::Handle)
# Tests:
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test)
BuildRequires: perl(Test::Harness)

%{?perl_default_filter}

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
			-name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc ChangeLog COPYING* NEWS README THANKS TODO
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
