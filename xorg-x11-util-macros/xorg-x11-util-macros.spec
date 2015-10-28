Summary: X.Org X11 Autotools macros
Name: xorg-x11-util-macros
Version: 1.19.0
Release: 2
License: The Open Group License
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/archive/individual/util/util-macros-%{version}.tar.bz2 
BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem

BuildArch: noarch

%description
X.Org X11 autotools macros required for building the various packages that
comprise the X Window System.

%prep
%setup -q -n util-macros-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%dir %{_datadir}/aclocal
#%{_datadir}/aclocal/xorgversion.m4
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc

%changelog
* Fri Oct 23 2015 cjacker - 1.19.0-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

