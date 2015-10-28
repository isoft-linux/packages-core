Name:           libglew
Version:        1.12.0
Release:        2 
Summary:        The OpenGL Extension Wrangler Library
License:        BSD and MIT
URL:            http://glew.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/glew/glew/%{version}/glew-%{version}.tgz
Patch0:         glew-fix-makefile.patch

BuildRequires:  libGLU-devel

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++
extension loading library. GLEW provides efficient run-time mechanisms for
determining which OpenGL extensions are supported on the target platform.
OpenGL core and extension functionality is exposed in a single header file.
GLEW is available for a variety of operating systems, including Windows, Linux,
Mac OS X, FreeBSD, Irix, and Solaris.

This package contains the demo GLEW utilities.  The libraries themselves
are in libGLEW and libGLEWmx.

%package devel
Summary:        Development files for glew library
Requires:       libGLU-devel

%description devel
Development files for glew library.


%prep
%setup -q -n glew-%{version}
%patch0 -p1

# update config.guess for new arch support
cp /usr/lib/rpm/config.guess config/

%build
make %{?_smp_mflags} CFLAGS.EXTRA="$RPM_OPT_FLAGS -fPIC" includedir=%{_includedir} STRIP= libdir=%{_libdir} bindir=%{_bindir} GLEW_DEST=

%install
make install.all GLEW_DEST= DESTDIR="$RPM_BUILD_ROOT" libdir=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.a" -delete

# fix perms
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/*.so*


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/libGLEW.so.*
%{_libdir}/libGLEWmx.so.*

%files devel
%{_libdir}/libGLEW.so
%{_libdir}/libGLEWmx.so
%{_libdir}/pkgconfig/glew.pc
%{_libdir}/pkgconfig/glewmx.pc
%{_includedir}/GL/*.h

%changelog
* Fri Oct 23 2015 cjacker - 1.12.0-2
- Rebuild for new 4.0 release

