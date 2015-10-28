Name:		man 
Version:	1.6g
Release:	2
Summary:	A utility for reading man pages
License:	GPL
URL:		http://primates.ximian.com/~flucifredi/man/
Source0:	%{name}-%{version}.tar.gz
Patch0:     man-troff.patch
Patch1:     man-fix-normal-user-install.patch

BuildRequires:	groff, gawk

%description
A utility for reading man pages

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./configure -confdir=/etc +suid +sgid +fhs +lang none
sed -i "s/\\/usr\\/bin\\/awk/\\/usr\\/bin\\/gawk/" ./conf_script
make


%install
make PREFIX=$RPM_BUILD_ROOT install || return 1
sed -i -e "s|-Tlatin1||g" \
        -e "s|less -is|less|g" \
        $RPM_BUILD_ROOT/etc/man.conf

%files
%{_sysconfdir}/man.conf
%{_bindir}/apropos
%{_bindir}/man
%{_bindir}/man2dvi
%{_bindir}/man2html
%{_bindir}/whatis
%{_sbindir}/makewhatis
%{_mandir}/man1/apropos.1.gz
%{_mandir}/man1/man.1.gz
%{_mandir}/man1/man2html.1.gz
%{_mandir}/man1/whatis.1.gz
%{_mandir}/man5/man.conf.5.gz
%{_mandir}/man8/makewhatis.8.gz


%changelog
* Fri Oct 23 2015 cjacker - 1.6g-2
- Rebuild for new 4.0 release


