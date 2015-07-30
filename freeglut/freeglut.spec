Summary:        A freely licensed alternative to the GLUT library
Name:           freeglut
Version:        3.0.0 
Release:        12
URL:            http://freeglut.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
License:        MIT
Group:          System Environment/Libraries
BuildRequires:  pkgconfig libGL-devel libXext-devel libXxf86vm-devel libGLU-devel
# The virtual Provides below is present so that this freeglut package is a
# drop in binary replacement for "glut" which will satisfy rpm dependancies
# properly.  The Obsoletes tag is required in order for any pre-existing
# "glut" package to be removed and replaced with freeglut when upgrading to
# freeglut.  Note: This package will NOT co-exist with the glut package.
Provides:       glut = 3.7
Obsoletes:      glut < 3.7

%description
freeglut is a completely open source alternative to the OpenGL Utility Toolkit
(GLUT) library with an OSI approved free software license. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL 'RedBook'. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, universally available and highly portable.

freeglut allows the user to create and manage windows containing OpenGL
contexts on a wide range of platforms and also read the mouse, keyboard and
joystick functions.


%package devel
Summary:        Freeglut developmental libraries and header files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGL-devel libGL-devel
Provides:       glut-devel = 3.7
Obsoletes:      glut-devel < 3.7

%description devel
Developmental libraries and header files required for developing or compiling
software which links to the freeglut library, which is an open source
alternative to the popular GLUT library, with an OSI approved free software
license.


%prep
%setup -q

%build
mkdir build 

pushd build
%cmake ..
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

#we do not ship static files.
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a
rpmclean

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/libglut*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/GL/*.h
%{_libdir}/libglut.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

