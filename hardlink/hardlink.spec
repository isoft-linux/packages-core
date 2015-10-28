Summary:	Create a tree of hardlinks
Name:		hardlink
Version:	1.0
Release:	2
Epoch:		1
URL:		http://pkgs.fedoraproject.org/gitweb/?p=hardlink.git
License:	GPL+
Source0:	hardlink.c
Source1:	hardlink.1
Obsoletes:	kernel-utils

%description
hardlink is used to create a tree of hard links.
It's used by kernel installation to dramatically reduce the
amount of diskspace used by each kernel package installed.

%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} hardlink.c

%build
gcc $RPM_OPT_FLAGS hardlink.c -o hardlink

%install
rm -rf $RPM_BUILD_ROOT
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/hardlink.1
install -D -m 755 hardlink $RPM_BUILD_ROOT%{_sbindir}/hardlink

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/hardlink
%{_mandir}/man1/hardlink.1*

%changelog
* Fri Oct 23 2015 cjacker - 1:1.0-2
- Rebuild for new 4.0 release

* Wed Dec 04 2013 Cjacker <cjacker@gmail.com>
- first build for new OS


