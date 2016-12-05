Name:		check
Version:	0.10.0
Release:	1
Summary:	A unit test framework for C
Source0:	http://download.sourceforge.net/check/%{name}-%{version}.tar.gz
License:	LGPLv2+
URL:		http://check.sourceforge.net/

%description
Check is a unit test framework for C. It features a simple interface for 
defining unit tests, putting little in the way of the developer. Tests 
are run in a separate address space, so Check can catch both assertion 
failures and code errors that cause segmentation faults or other signals. 
The output from unit tests can be used within source code editors and IDEs.

%package devel
Summary:	Libraries and headers for developing programs with check
Requires:	pkgconfig
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and headers for developing programs with check

%package static
Summary:        Static libraries of check

%description static
Static libraries of check.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

sed -i 's@#! /bin/gawk@#! /usr/bin/gawk@g' $RPM_BUILD_ROOT/%{_bindir}/checkmk

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}

# redundant files
rm -f $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/COPYING.LESSER
rm -f $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/ChangeLog*
rm -f $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/NEWS
rm -f $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/README
rm -f $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/SVNChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.LESSER ChangeLog ChangeLogOld NEWS README SVNChangeLog
%{_libdir}/libcheck.so.*
%{_bindir}/checkmk
%{_mandir}/man1/checkmk.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/check.h
%{_includedir}/check_stdint.h
%{_defaultdocdir}/%{name}/example/
%{_libdir}/libcheck.so
%{_libdir}/pkgconfig/check.pc
%{_datadir}/doc/%{name}
%{_datadir}/aclocal/check.m4

#check used to be static only, hence this.
%files static
%defattr(-,root,root,-)
%{_libdir}/libcheck.a

%changelog
* Mon Dec 05 2016 sulit - 0.10.0-1
- update check to 0.10.0

* Fri Oct 23 2015 cjacker - 0.9.13-3
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

