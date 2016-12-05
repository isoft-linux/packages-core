Summary: Modify rpath of compiled programs
Name: chrpath
Version: 0.16
Release: 1
License: GPL+
URL: ftp://ftp.hungry.com/pub/hungry/chrpath/
Source0: ftp://ftp.hungry.com/pub/hungry/chrpath/%{name}-%{version}.tar.gz

%description
chrpath allows you to modify the dynamic library load path (rpath) of
compiled programs.  Currently, only removing and modifying the rpath
is supported.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}/usr/doc
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*


%changelog
* Mon Dec 05 2016 sulit - 0.16-1
- upgrade chrpath to 0.16

* Fri Oct 23 2015 cjacker - 0.13-4
- Rebuild for new 4.0 release

