Summary: Displays where a particular program in your path is located.
Name: which
Version: 2.16
Release: 6.2.1
License: GPL
Group:  Core/Runtime/Utility 
Source0: http://www.xs4all.nl/~carlo17/which/%{name}-%{version}.tar.gz
Source1: which-2.sh
Url: http://www.xs4all.nl/~carlo17/which/
Patch: which-2.13-afs.patch
Patch1: which-2.14-broken.patch
Prefix: %{_prefix}

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%prep
%setup -q
%patch -p1 -b .afs
%patch1 -p1 -b .broken

%build
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/profile.d
rm -rf $RPM_BUILD_ROOT%{_infodir}

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%config /etc/profile.d/which-2.*
%{_mandir}/*/*

%changelog
