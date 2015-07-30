Summary: Access control list utilities.
Name: acl
Version: 2.2.52
Release: 1
License: GPL
Group:   Core/Runtime/Utility 
URL: http://oss.sgi.com/projects/xfs/
Source0: http://download.savannah.gnu.org/releases/acl/%{name}-%{version}.src.tar.gz
Patch1: 0001-acl-2.2.49-bz675451.patch
Patch3: 0003-acl-2.2.52-tests.patch
Patch4: 0004-acl-2.2.52-libdir.patch
Patch5: 0005-acl-2.2.52-getfacl-segv.patch

BuildRequires: libattr-devel >= 2.4.1

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support.
License: LGPL
Group:   Core/Runtime/Library 
Requires(pre): /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Access control list static libraries and headers.
License: LGPL
Group:  Core/Development/Library 
Requires: libacl, libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure --libdir=%{_libdir} --libexecdir=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# remove useless docs
rm -rf $RPM_BUILD_ROOT/usr/share/doc

%find_lang acl
rpmclean

%check
#some filesystem may not support acl/attr completely
#some testcases will fail
if ./setfacl/setfacl -m u:`id -u`:rwx .; then
    make tests ||:
else
    echo '*** ACLs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi


%clean
rm -rf $RPM_BUILD_ROOT

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f acl.lang 
%defattr(-,root,root)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%defattr(-,root,root)
%{_libdir}/libacl.so
%{_libdir}/libacl.a
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_libdir}/libacl.*
%{_mandir}/man3/acl_*

%files -n libacl
%defattr(-,root,root)
%{_libdir}/libacl.so.*
