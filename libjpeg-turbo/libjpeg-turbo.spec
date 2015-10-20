Name:		libjpeg-turbo
Version:	1.4.2
Release:    1	
Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files

Group:		System Environment/Libraries
License:	IJG
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	autoconf, automake, libtool
BuildRequires:  yasm
Provides:	libjpeg 

Patch0:		libjpeg-turbo12-noinst.patch

%description
The libjpeg-turbo package contains a library of functions for manipulating
JPEG images.

%package devel
Summary:	Headers for the libjpeg-turbo library
Group:		Development/Libraries
Provides:	libjpeg-devel 
Requires:	libjpeg-turbo = %{version}-%{release}

%description devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the libjpeg-turbo library.

%package utils
Summary:	Utilities for manipulating JPEG images
Group:		Applications/Multimedia
Requires:	libjpeg-turbo = %{version}-%{release}

%description utils
The libjpeg-turbo-utils package contains simple client programs for
accessing the libjpeg functions. It contains cjpeg, djpeg, jpegtran,
rdjpgcom and wrjpgcom. Cjpeg compresses an image file into JPEG format.
Djpeg decompresses a JPEG file into a regular image file. Jpegtran
can perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%package static
Summary:	Static version of the libjpeg-turbo library
Group:		Development/Libraries
Provides:	libjpeg-static
Requires:	libjpeg-turbo-devel = %{version}-%{release}

%description static
The libjpeg-turbo-static package contains static library for manipulating
JPEG images.

%package -n turbojpeg
Summary:	TurboJPEG library
Group:		System Environment/Libraries

%description -n turbojpeg
The turbojpeg package contains the TurboJPEG shared library.

%package -n turbojpeg-devel
Summary:	Headers for the TurboJPEG library
Group:		Development/Libraries
Requires:	turbojpeg = %{version}-%{release}

%description -n turbojpeg-devel
This package contains header files necessary for developing programs which
will manipulate JPEG files using the TurboJPEG library.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Don't distribute libjpegturbo.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libturbojpeg.a
rm -rf $RPM_BUILD_ROOT%{_bindir}/tjbench
rm -rf $RPM_BUILD_ROOT%{_docdir}/*

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%check
make test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n turbojpeg -p /sbin/ldconfig
%postun -n turbojpeg -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libjpeg.so.62*

%files devel
%defattr(-,root,root,-)
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_libdir}/libjpeg.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files static
%defattr(-,root,root,-)
%{_libdir}/libjpeg.a

%files -n turbojpeg
%{_libdir}/libturbojpeg.so.0*

%files -n turbojpeg-devel
%{_includedir}/turbojpeg.h
%{_libdir}/libturbojpeg.so

%changelog
* Thu Oct 08 2015 Cjacker <cjacker@foxmail.com>
- update to 1.4.2

