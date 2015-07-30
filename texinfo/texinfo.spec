Name:	    texinfo 
Version:	5.2
Release:	1
Summary:	GNU documentation system for on-line information and printed output

Group:		Core/Runtime/Utility
License:    GPL	
URL:		http://www.gnu.org/software/texinfo
Source0:	%{name}-%{version}.tar.xz
Patch0:     texinfo-5.2-C-n-fix.patch
%description
%{summary}

%prep
%setup -q
%patch0 -p0

%build
%configure
make %{?_smp_mflags}
%install
make install DESTDIR=%{buildroot}
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

mkdir %{buildroot}/sbin
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin/

%find_lang texinfo_document 
%find_lang texinfo
cat texinfo_document.lang >>texinfo.lang

rpmclean

%files -f texinfo.lang
/sbin/install-info
%{_bindir}/info
%{_bindir}/infokey
%{_bindir}/makeinfo
%{_bindir}/pdftexi2dvi
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/texindex
%{_infodir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%dir %{_datadir}/texinfo
%{_datadir}/texinfo/*

