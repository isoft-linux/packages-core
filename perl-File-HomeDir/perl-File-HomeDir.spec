Name:           perl-File-HomeDir
Version:        1.00
Release:        1%{?dist}
Summary:        Find your home and other directories on any platform
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-HomeDir/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/File-HomeDir-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd) >= 3.12
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(ExtUtils::MM_Unix)
BuildRequires:  perl(File::Path) >= 2.01
BuildRequires:  perl(File::Spec) >= 3.12
# POSIX not used on Linux
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp) >= 0.19
#BuildRequires:  perl(File::Which) >= 0.05
# Mac::Files not used on Linux
# Mac::SystemDirectory not used on Linux
# Win32 not used on Linux
# Tests:
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 0.47
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Cwd) >= 3.12
Requires:       perl(Exporter)
Requires:       perl(File::Path) >= 2.01
Requires:       perl(File::Spec) >= 3.12
Requires:       perl(File::Temp) >= 0.19
#Requires:       perl(File::Which) >= 0.05

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude}|perl\\(Cwd\\)|perl\\(File::Path\\)|perl\\(File::Spec\\)|perl\\(File::Temp\\)|perl\\(File::Which\\)|perl\\(Mac::|perl\\(Win32

%description
File::HomeDir is a module for locating the directories that are "owned"
by a user (typically your user) and to solve the various issues that
arise trying to find them consistently across a wide variety of
platforms.

%prep
%setup -q -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test || :

%files
%doc Changes LICENSE README
%{perl_vendorlib}/File/
%{_mandir}/man3/*.3pm*

%changelog
* Mon Dec 19 2016 sulit - 1.00-1
- add perl-File-HomeDir to core group

