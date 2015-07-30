Summary: A tool for converting XML files to various formats
Name: xmlto
Version: 0.0.26
Release: 2
License: GPLv2
Group:   CoreDev/Development/Utility/Documentation
#Older versions up to xmlto-0.0.20
#URL: http://cyberelk.net/tim/xmlto/
#Source0: http://cyberelk.net/tim/data/xmlto/stable/%{name}-%{version}.tar.bz2
URL: https://fedorahosted.org/xmlto/
Source0: http://svn.fedorahosted.org/svn/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: docbook-xsl >= 1.56.0
BuildRequires: /usr/bin/xsltproc
BuildRequires: util-linux, flex

# We rely heavily on the DocBook XSL stylesheets!
Requires: docbook-xsl >= 1.56.0
Requires: text-www-browser
Requires: /usr/bin/xsltproc
Requires: docbook-dtds
Requires: util-linux, flex

%description
This is a package for converting XML files to various formats using XSL
stylesheets.

%prep
%setup -q

%build
touch doc/xmlto.xml doc/xmlif.xml
%configure
make

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto
%exclude %{_datadir}/xmlto/format/fo/dvi
%exclude %{_datadir}/xmlto/format/fo/ps
%exclude %{_datadir}/xmlto/format/fo/pdf

#%files tex
#%defattr(-,root,root)
#%{_datadir}/xmlto/format/fo/dvi
#%{_datadir}/xmlto/format/fo/ps
#%{_datadir}/xmlto/format/fo/pdf

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

