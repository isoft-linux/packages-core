Name: intltool
Summary: Utility for internationalizing various kinds of data files.
Version: 0.51.0
Release: 3
License: GPL
Source: %{name}-%{version}.tar.gz
URL:    http://freedesktop.org/wiki/Software/intltool/ 
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: patch
Requires: gettext

BuildArch: noarch

Obsoletes: xml-i18n-tools
Provides: xml-i18n-tools = 0.11

%description
This tool automatically extracts translatable strings from oaf, glade,
bonobo ui, nautilus theme, .desktop, and other data files and puts
them in the po files.

%prep
%setup -q

%build
%configure

make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall

%check
make check

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/intltool
%{_datadir}/aclocal/*
%{_mandir}/man*/*

%changelog
* Wed Nov 04 2015 kun.li@i-soft.com.cn - 0.51.0-3
- ADD Requires: gettext

* Fri Oct 23 2015 cjacker - 0.51.0-2
- Rebuild for new 4.0 release

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
