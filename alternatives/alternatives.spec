Summary: alternatives management system.
Name: alternatives 
Version: 1.8
Release: 1
License: GPLv2
Source: http://fedorahosted.org/releases/c/h/chkconfig/chkconfig-%{version}.tar.bz2

%description
Alternatives system creates a way for several programs that 
fulfill the same or similar functions to be listed as alternative implementations 
that are installed simultaneously but with one particular implementation designated as the default. 

%prep
%setup -q -n chkconfig-%{version}

%build
gcc -o alternatives alternatives.c -DVERSION=\"%{version}\"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/alternatives
mkdir -p $RPM_BUILD_ROOT/etc/alternatives

install -D -m0755 alternatives $RPM_BUILD_ROOT/%{_sbindir}/alternatives
install -D -m0755 alternatives $RPM_BUILD_ROOT/%{_sbindir}/update-alternatives

install -D -m0644 alternatives.8 $RPM_BUILD_ROOT/%{_mandir}/man8/alternatives.8
install -D -m0644 alternatives.8 $RPM_BUILD_ROOT/%{_mandir}/man8/update-alternatives.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /etc/alternatives
%{_sbindir}/update-alternatives
%{_sbindir}/alternatives
%dir /var/lib/alternatives
%{_mandir}/*/update-alternatives*
%{_mandir}/*/alternatives*

%changelog
* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 1.8-1
- update alternatives to 1.8

* Fri Oct 23 2015 cjacker - 1.5-3
- Rebuild for new 4.0 release
