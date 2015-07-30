Name:		init-scripts
Version:	0.1
Release:	1
Summary:	System lang settings scripts

License:    GPL	
Source0:    lang-scripts-%{version}.tar.gz	
#some old rh style script need it.
Source1:    functions
 
BuildRequires: gcc	
%description
%{summary}

%prep
%setup -q -n lang-scripts-%{version}

%build
make CC=gcc

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/
%files
%{_sysconfdir}/init.d/functions
/sbin/consoletype
%{_mandir}/man1/consoletype.1*
%{_sysconfdir}/profile.d/lang.sh


%changelog

