Summary: Text file format converter
Name: dos2unix
Version: 7.3.4
Release: 1
License: Freely distributable
Source: http://waterlan.home.xs4all.nl/%{name}/%{name}-%{version}.tar.gz

BuildRequires: gettext
Provides: unix2dos = %{version}-%{release}
Obsoletes: unix2dos < 5.1-1

%description
Dos2unix converts DOS or MAC text files to UNIX format.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

# We add doc files manually to %%doc
rm -rf $RPM_BUILD_ROOT%{_docdir}

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc man/man1/dos2unix.htm  ChangeLog.txt COPYING.txt
%doc NEWS.txt README.txt TODO.txt
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_bindir}/unix2dos
%{_bindir}/unix2mac
%{_mandir}/man1/*.1*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Dec 07 2016 sulit - 7.3.4-1
- upgrade dos2unix to 7.3.4
- remove all older patches
- add BuildRequires gettext

* Fri Oct 23 2015 cjacker - 3.1-25.2.1
- Rebuild for new 4.0 release

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
