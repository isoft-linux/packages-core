Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.2
Release: 2 
License: MIT
Source: ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
Patch0: libxml2-upstream-fix.patch

BuildRequires: python python-devel zlib-devel pkgconfig
URL: http://xmlsoft.org/
%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Requires: libxml2 = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package static
Summary: Static library for libxml2
Requires: libxml2 = %{version}-%{release}

%description static
Static library for libxml2 provided for specific uses or shaving a few
microseconds when parsing, do not link to them for generic purpose packages.

%package -n python-libxml2
Summary: Python bindings for the libxml2 library
Requires: libxml2 = %{version}-%{release}

%description -n python-libxml2
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{_smp_mflags}

%install
rm -fr %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*
%doc %{_mandir}/man3/libxml.3*

%{_libdir}/lib*.so.*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%files devel
%defattr(-, root, root)
%{_mandir}/man1/xml2-config.1*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/*.a
%{_datadir}/gtk-doc/html/libxml2
%{_docdir}/libxml2-%{version}
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%files -n python-libxml2
%defattr(-, root, root)
%{_libdir}/python*/site-packages/libxml2.py*
%{_libdir}/python*/site-packages/drv_libxml2.py*
%{_libdir}/python*/site-packages/libxml2mod*
%{_docdir}/libxml2-python-%{version}
%changelog
* Fri Oct 23 2015 cjacker - 2.9.2-2
- Rebuild for new 4.0 release

