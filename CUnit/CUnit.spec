%global tarver 2.1-3

Name:           CUnit
Version:        2.1.3
Release:        2%{?dist}
Summary:        Unit testing framework for C
License:        LGPLv2+
URL:            http://cunit.sourceforge.net/
Source0:        http://downloads.sourceforge.net/cunit/%{name}-%{tarver}.tar.bz2

BuildRequires:  automake
BuildRequires:  libtool

%description 
CUnit is a lightweight system for writing, administering,
and running unit tests in C.  It provides C programmers a basic
testing functionality with a flexible variety of user interfaces.

%package devel
Summary:        Header files and libraries for CUnit development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -q -n %{name}-%{tarver}
find -name *.c -exec chmod -x {} \;

%build
autoreconf -f -i
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f `find %{buildroot} -name *.la`

# work around bad docdir= in doc/Makefile*
mkdir -p %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_prefix}/doc/%{name} %{buildroot}%{_docdir}/%{name}/html

# add some doc files into the buildroot manually (#1001276)
for f in AUTHORS ChangeLog COPYING NEWS README TODO VERSION ; do
    install -p -m0644 -D $f %{buildroot}%{_docdir}/%{name}/${f}
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_datadir}/%{name}/
%{_libdir}/libcunit.so.*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/TODO
%{_docdir}/%{name}/VERSION

%files devel
%{_docdir}/%{name}/html/
%{_includedir}/%{name}/
%{_libdir}/libcunit.so
%{_libdir}/pkgconfig/cunit.pc
%{_mandir}/man3/CUnit.3*

%changelog
* Sun Nov 15 2015 Cjacker <cjacker@foxmail.com> - 2.1.3-2
- Initial build

