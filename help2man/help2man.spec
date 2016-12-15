Name:		help2man
Version:    1.47.4
Release:	1
Summary:    Conversion tool to create man files	

License:	GPL
URL:		http://www.gnu.org/software/help2man/
Source0:	http://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(strict)

%description
%{summary}

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
#we do not ship any info files  
rm -rf $RPM_BUILD_ROOT%{_infodir}

#we do not ship any locale man pages
rm -rf $RPM_BUILD_ROOT%{_mandir}/{[a-l]*,[n-z]*}

%find_lang help2man

%files -f help2man.lang
%{_bindir}/help2man
%{_libdir}/help2man
%{_mandir}/man1/help2man.1.gz

%changelog
* Thu Dec 15 2016 sulit - 1.47.4-1
- update help2man to 1.47.4

* Fri Oct 23 2015 cjacker - 1.47.1-2
- Rebuild for new 4.0 release


