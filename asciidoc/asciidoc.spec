Name: asciidoc		
Version: 8.6.9	
Release: 1
Summary: Text document format for short documents, articles, books and UNIX man pages

Group:	CoreDev/Development/Utility/Documentation	
License: GPL
URL:		http://www.methods.co.nz/asciidoc/
Source0:    http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/%{name}-%{version}.tar.gz

Requires:   python, libxslt	

%description

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%dir %{_sysconfdir}/asciidoc
%{_sysconfdir}/asciidoc/*
%{_bindir}/a2x
%{_bindir}/a2x.py
%{_bindir}/asciidoc
%{_bindir}/asciidoc.py
%{_mandir}/man1/a2x.1.gz
%{_mandir}/man1/asciidoc.1.gz


%changelog

