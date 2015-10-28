%global svnversion 16
%global soname     libclrun.so.%{version}.%{svnversion}

Name:           opencl-utils
Version:        0
Release:        16.svn%{svnversion}%{?dist}
Summary:        Useful OpenCL tools and utilities

License:        MIT
Url:            http://code.google.com/p/%{name}
###Commands to grab source from svn:
#svn co -r 16 http://opencl-utils.googlecode.com/svn/trunk/ opencl-utils
#tar -Jcv --exclude-vcs -f opencl-utils.tar.xz opencl-utils
#rm -f -r opencl-utils
Source0:         %{name}.tar.xz
Source2:         %{name}.pc
#Kudos to Alec Leamas: http://code.google.com/p/opencl-utils/issues/detail?id=2
Patch0:         %{name}-fixupmakefile.patch

BuildRequires:  mesa-libGL-devel
BuildRequires:  perl

%package        devel
Summary:        Devel files for OpenCL Utils
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description
#Modified from the homepage
OpenCL Utils is a project that aims to create various tools and utilities to
make the use of OpenCL more useful and efficient, such as: useful functions,
optimization hints and common kernel templates. This package currently only
contains CLRun, which allows for dynamic loading of OpenCL.

%description devel
This package includes the headers files for OpenCL Utils.
OpenCL Utils is a project that aims to create various tools and utilities to
make the use of OpenCL more useful and efficient, such as: useful functions,
optimization hints and common kernel templates.

%prep
%setup -q -n %{name}
%patch0 -p0
#Fixes for Example compiling
sed -i -e 's/@version@/%{version}/' -e 's|@prefix@|%{_prefix}|' %{SOURCE2}
sed -i 's/\r//' examples/clrun-example/example2.cpp
sed -i '/ldl/c\\tgcc $(pkg-config --cflags --libs opencl-utils) example1.c' examples/clrun-example/Makefile
sed -i '/lclrun/c\\tg++ $(pkg-config --cflags --libs opencl-utils) example2.cpp' examples/clrun-example/Makefile
#To avoid copying a windows build file later on
rm -f examples/OCLUtilsExamples.vcproj
#Clean the generated files before compiling
cd src/clrun/
make clean

%build
cd src/clrun/
env CFLAGS="%{optflags} -fPIC -Wl,-soname=%{soname}" make

%install
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}/%{name}/clrun/
cp -a src/clrun/*.h %{buildroot}%{_includedir}/%{name}/clrun/
cp -a src/clrun/*.c %{buildroot}%{_includedir}/%{name}/clrun/
cp -a src/clrun/Makefile %{buildroot}%{_includedir}/%{name}/clrun/
cp -a src/clrun/generateClRun.pl %{buildroot}%{_includedir}/%{name}/clrun/
cp -r src/include %{buildroot}%{_includedir}/%{name}/
install -m 0644 -D %{SOURCE2} %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
#install the library and the links
soname=%{soname}
install -p -D -m 0755 src/clrun/${soname%%.*.*} %{buildroot}%{_libdir}/%{soname}
cd %{buildroot}%{_libdir}
ln -sf  $soname ${soname%%.*}
ln -sf  $soname ${soname%%.*.*}

%files
%{_libdir}/*.so.*

%files devel
%doc examples/*
%{_includedir}/%{name}/include/CL
%{_includedir}/%{name}/clrun/
%{_includedir}/%{name}/include/clrun.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri Oct 23 2015 cjacker - 0-16.svn16
- Rebuild for new 4.0 release

