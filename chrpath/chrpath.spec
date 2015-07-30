Summary: Modify rpath of compiled programs
Name: chrpath
Version: 0.13
Release: 3
License: GPL+
Group:  CoreDev/Development/Utility 
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
rpmclean
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

