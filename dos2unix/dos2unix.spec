Summary: Text file format converter
Name: dos2unix
Version: 3.1
Release: 25.2.1
License: Freely distributable
Source: %{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}.patch
Patch1: dos2unix-3.1-segfault.patch
Patch2: dos2unix-3.1-safeconv.patch
Patch3: dos2unix-3.1-manpage-update-57507.patch
Patch4: dos2unix-3.1-preserve-file-modes.patch
Patch5: dos2unix-3.1-tmppath.patch

Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Dos2unix converts DOS or MAC text files to UNIX format.

%prep
%setup -q
%patch0 -p1 -b .orig
%patch1 -p1 -b .segfault
%patch2 -p1 -b .safeconv
%patch3 -p1 -b .manpage-update-57507
%patch4 -p1 -b .preserve-file-modes
%patch5 -p1 -b .tmppath

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
* Fri Oct 23 2015 cjacker - 3.1-25.2.1
- Rebuild for new 4.0 release

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
