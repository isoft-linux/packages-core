Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.69
Release:    4 
License:    GPLv2+ and GFDL
Group:      CoreDev/Development/Utility 
Source:     http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
Source1:    filter-provides-autoconf.sh
Source2:    filter-requires-autoconf.sh
URL:        http://www.gnu.org/software/autoconf/
BuildRequires:      m4 >= 1.4.7
Requires:           m4 >= 1.4.7
BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# filter out bogus perl(Autom4te*) dependencies
%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q
%build
# use ./configure here to avoid copying config.{sub,guess} with those from the
# rpm package
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
  --bindir=%{_bindir} --datadir=%{_datadir}
make #  %{?_smp_mflags}  The Makefile is not smp safe.

%check
#make check VERBOSE=yes

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/autoconf/
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%changelog
