%define api_version 1.14.1

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake
Version:    %{api_version}
Release:    4
License:    GPLv2+ and GFDL and MIT 
Source:     http://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz
Source1:    filter-provides-automake.sh
Source2:    filter-requires-automake.sh
Source3:    automake.man
Source4:    aclocal.man
URL:        http://sources.redhat.com/automake
Requires:   autoconf >= 2.62
Buildrequires:  autoconf >= 2.62
BuildArch:  noarch
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE1}
%define __find_requires %{SOURCE2}

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles. If you install Automake, you will also need to install
GNU's Autoconf package.

%prep
%setup -q -n automake-%{version}

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
   --bindir=%{_bindir} --datadir=%{_datadir} --libdir=%{_libdir} \
   --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man1/automake.1
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_mandir}/man1/aclocal.1

# create this dir empty so we can own it
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/aclocal
rm -rf $RPM_BUILD_ROOT%{_infodir}

#%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS NEWS
%{_bindir}/*
#%{_datadir}/automake-%{api_version}
#%{_datadir}/aclocal-%{api_version}
%{_datadir}/automake-*
%{_datadir}/aclocal-*
%{_mandir}/man1/*
%dir %{_datadir}/aclocal

%changelog
* Fri Oct 23 2015 cjacker - 1.14.1-4
- Rebuild for new 4.0 release

