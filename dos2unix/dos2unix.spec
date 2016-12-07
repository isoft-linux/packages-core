Summary: Text file format converter
Name: dos2unix
Version: 7.3.4
Release: 1
License: Freely distributable
Source: http://waterlan.home.xs4all.nl/%{name}/%{name}-%{version}.tar.gz

Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gettext

%description
Dos2unix converts DOS or MAC text files to UNIX format.

%prep
%setup -q

for I in *.[ch]; do
	sed -e 's,#endif.*,#endif,g' -e 's,#else.*,#else,g' $I > $I.new
	mv -f $I.new $I
done

%build
make clean
make CFLAGS="$RPM_OPT_FLAGS" 
make link

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install -m755 dos2unix $RPM_BUILD_ROOT%{_bindir}
install -m755 mac2unix $RPM_BUILD_ROOT%{_bindir}
install -m444 dos2unix.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -m444 mac2unix.1 $RPM_BUILD_ROOT%{_mandir}/man1

%files
%defattr(-,root,root,0755)
%doc COPYRIGHT
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_mandir}/*/*

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
