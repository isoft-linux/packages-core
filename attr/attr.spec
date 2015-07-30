Summary: Utilities for managing filesystem extended attributes.
Name: attr
Version: 2.4.47
Release: 10 
License: GPL
Group:  Core/Runtime/Utility 
Source: http://ftp.twaren.net/Unix/NonGNU//attr/%{name}-%{version}.src.tar.gz
Patch1: 0001-attr-2.4.47-warnings.patch
Patch2: 0002-attr-2.4.47-xattr-conf.patch
Patch3: attr-fix-headers.patch

Requires(pre): /sbin/ldconfig

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr
Summary: Dynamic library for extended attribute support.
Group:  Core/Runtime/Library 
License: LGPL
Requires(pre): /sbin/ldconfig

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%package -n libattr-devel
Summary: Extended attribute static libraries and headers.
Group:  Core/Development/Library 
License: LGPL
Requires: libattr

%description -n libattr-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
%configure 
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# remove useless doc
rm -rf $RPM_BUILD_ROOT/%{_docdir}

%find_lang attr

rpmclean

%check
#different filesystem may not support attr/acl completely.
#So some testcases will fail.
if ./setfattr/setfattr -n user.name -v value .; then
    make tests ||: 
else
    echo '*** xattrs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f attr.lang
%defattr(-,root,root)
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*
%{_mandir}/man5/attr.5*

%files -n libattr-devel
%defattr(-,root,root)
%{_libdir}/libattr.so
%{_includedir}/attr
%{_libdir}/libattr.*
%{_mandir}/man2/*attr.2*
%{_mandir}/man3/attr_*.3.*

%files -n libattr
%{_libdir}/libattr.so.*
%config(noreplace) %{_sysconfdir}/xattr.conf

