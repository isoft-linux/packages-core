Name:           cloog
%global         tarball_name %{name}
Version:        0.18.4
Release:        1%{?dist}
Epoch:		1
Summary:        The Chunky Loop Generator

License:        GPLv2+
URL:            http://www.cloog.org

# This tarball was retrieved directly from the Git source code
# repository of the Cloog project by doing:
#
#    git clone git://repo.or.cz/cloog.git -b cloog-0.18.3 cloog-0.18.3
#    tar -cvf cloog-0.18.3.tar.gz cloog-0.18.3

Source0:        cloog-0.18.4.tar.gz

BuildRequires:  isl-devel >= 0.12
BuildRequires:  gmp-devel >= 4.1.3
BuildRequires:  libtool
Obsoletes:	cloog-ppl cloog-ppl-devel

Requires(post): info
Requires(preun): info

%description
CLooG is a software which generates loops for scanning Z-polyhedra. That is,
CLooG finds the code or pseudo-code where each integral point of one or more
parametrized polyhedron or parametrized polyhedra union is reached. CLooG is
designed to avoid control overhead and to produce a very efficient code.

%package devel
Summary:        Development tools for the Chunky Loop Generator
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       isl-devel >= 0.12, gmp-devel >= 4.1.3

%description devel
The header files and dynamic shared libraries of the Chunky Loop Generator.

%prep
%setup -q -n %{tarball_name}-%{version}

%build
#./autogen.sh
%configure \
    --with-isl=system \
    --with-isl-prefix=%{_prefix}

# Remove the -fomit-frame-pointer compile flag
# Use system libtool to disable standard rpath
make %{?_smp_mflags} AM_CFLAGS= LIBTOOL=%{_bindir}/libtool

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"


rm %{buildroot}%{_libdir}/*/*.cmake

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/cloog
%{_libdir}/libcloog-isl.so.*

%files devel
%{_includedir}/cloog
%{_libdir}/libcloog-isl.so
%{_libdir}/pkgconfig/cloog-isl.pc
%exclude %{_libdir}/libcloog-isl.a
%exclude %{_libdir}/libcloog-isl.la

%changelog
* Mon Dec 05 2016 sulit - 1:0.18.4-1
- upgrade cloog to 0.18.4
- remove autogen gen configure stage

* Fri Oct 23 2015 cjacker - 1:0.18.3-3
- Rebuild for new 4.0 release

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build.
