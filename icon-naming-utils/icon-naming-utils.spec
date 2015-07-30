
Name:           icon-naming-utils
Version:        0.8.90
Release:        1
Summary: 	    A script to handle icon names in desktop icon themes

Group:          CoreDev/Development/Utility
License:        GPL 
BuildArch:	noarch
URL:            http://tango-project.org/Standard_Icon_Naming_Specification
Source0:        icon-naming-utils-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-XML-Simple
Requires:       perl-XML-Simple

Patch0:		icon-naming-utils-0.6.7-paths.patch

%description
A script for creating a symlink mapping for deprecated icon names to
the new Icon Naming Specification names, for desktop icon themes.

%prep
%setup -q
%patch0 -p1 -b .paths


%build
# the paths patch patches Makefile.am
aclocal
automake
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/icon-name-mapping
%{_datadir}/icon-naming-utils
%{_datadir}/pkgconfig/icon-naming-utils.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

