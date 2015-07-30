Name:		help2man
Version:    1.47.1	
Release:	1
Summary:    Conversion tool to create man files	

Group:	    CoreDev/Development/Utility/Documentation	
License:	GPL
URL:		http://www.gnu.org/software/help2man/
Source0:	http://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz

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

