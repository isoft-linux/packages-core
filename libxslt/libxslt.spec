Summary: Library providing the Gnome XSLT engine
Name: libxslt
Version: 1.1.28
Release: 2
License: MIT
Source: ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.gz
URL: http://xmlsoft.org/XSLT/
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: python-libxml2

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%package devel
Summary: Development files for %{name}
Requires: libxslt = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python-libxslt
Summary: Python bindings for the libxslt library
Requires: libxslt = %{version}-%{release}
Requires: python-libxml2

%description -n python-libxslt
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the python-libxml2
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.

%prep
%setup -q

chmod 644 python/tests/*

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%check 
#make tests

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%doc %{_mandir}/man1/xsltproc.1*
%{_libdir}/lib*.so.*
%{_libdir}/libxslt-plugins
%{_bindir}/xsltproc

%files devel
%defattr(-, root, root,-)
%doc %{_mandir}/man3/libxslt.3*
%doc %{_mandir}/man3/libexslt.3*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_datadir}/aclocal/libxslt.m4
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/libxslt.pc
%{_libdir}/pkgconfig/libexslt.pc
%{_docdir}/libxslt-%{version}

%files -n python-libxslt
%defattr(-, root, root,-)
%{python_sitearch}/libxslt.py*
%{python_sitearch}/libxsltmod*
%doc python/libxsltclass.txt
%doc python/tests/*.py
%doc python/tests/*.xml
%doc python/tests/*.xsl
%{_docdir}/libxslt-python-%{version}
%changelog
* Fri Oct 23 2015 cjacker - 1.1.28-2
- Rebuild for new 4.0 release

