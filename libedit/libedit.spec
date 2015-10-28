%define snap 20150325

Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.1
Release:    5
License:	BSD
URL:		http://www.thrysoee.dk/editline/
Source0:	http://www.thrysoee.dk/editline/%{name}-%{snap}-%{version}.tar.gz

BuildRequires:	gawk
BuildRequires:	ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD Editline library.
It provides generic line editing, history, and tokenization functions, similar
to those found in GNU Readline.

%package devel
Summary:	Development files for %{name}

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	ncurses-devel

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n %{name}-%{snap}-%{version}

%build
%configure --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/histedit.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%dir %{_includedir}/editline
%{_includedir}/editline/readline.h

%{_mandir}/man3/*
%{_mandir}/man5/editrc.5*

%changelog
* Fri Oct 23 2015 cjacker - 3.1-5
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

