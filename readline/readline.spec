Summary: A library for editing typed command lines
Name: readline
Version: 6.3
Release: 1 
License: GPL
Group:  Core/Runtime/Library
URL: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source: ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
#upstream patch
Patch0:readline63-001       
Patch1:readline63-002       
Patch2:readline63-003       
Patch3:readline63-004       
Patch4:readline63-005       
Patch5:readline63-006       
Patch6:readline63-007     
Patch7:readline63-008       
Patch8:readline-link-to-tinfo.patch

BuildRequires: ncurses-devel

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library
Group: Core/Development/Library
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%package static
Summary: Static libraries for the readline library
Group:  Core/Development/Library
Requires: %{name}-devel = %{version}-%{release}

%description static
The readline-static package contains the static version of the readline
library.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0

%patch8 -p1
%build
export CPPFLAGS="-I/usr/include/ncurses"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT%{_datadir}/readline
rm -rf $RPM_BUILD_ROOT%{_infodir}

rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%{_libdir}/libhistory*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/readline
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%changelog
