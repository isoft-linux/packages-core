Summary: Modern Version Control System designed to replace CVS
Name: subversion
Version: 1.8.8
Release: 1   
License: BSD
Group: CoreDev/Development/Utility
URL: http://subversion.tigris.org/
Source0: http://subversion.tigris.org/tarballs/subversion-%{version}.tar.bz2
Source1: svn-editor.sh

BuildRequires: apr-util-devel
BuildRequires: apr-devel
BuildRequires: libserf-devel
Requires:	apr
Requires:	apr-util
Requires:   libserf

%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file.  Subversion is intended to be a
compelling replacement for CVS.

%package devel
Summary: Libraries and headers for adding subverion support to applications 
Group: CoreDev/Development/Library
Requires:	subversion

%description devel
This package contains various headers accessing some subversion functionality
from applications.

%prep
%setup -q

%build
%configure \
    --without-sasl \
    --without-swig \
    --without-gnome-keyring \
    --enable-bdb6 \
    --disable-static
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/profile.d

%find_lang subversion

rpmclean

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f subversion.lang
%defattr(-,root,root)
%{_mandir}/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_sysconfdir}/profile.d/svn-editor.sh

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%dir %{_includedir}/subversion-1
%{_includedir}/subversion-1/*


#%files -n mod_dav_svn
#%defattr(-,root,root)
#/etc/httpd/conf.d/subversion.conf
#/usr/lib/httpd/modules
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

