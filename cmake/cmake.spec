Name: cmake
Version: 3.7.1
Release: 1 
Summary: Cross-platform make system

License: BSD
URL: http://www.cmake.org
Source0: http://www.cmake.org/files/v3.3/cmake-%{version}.tar.gz
Source2: macros.cmake
Source3: cmake-init.el
Patch0: cmake-set-lib-to-usr_lib.patch

BuildRequires:  expat-devel, zlib-devel, libcurl-devel
BuildRequires:  gcc-gfortran
BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  bzip2-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  libarchive-devel
BuildRequires:  python-sphinx
BuildRequires:  xz-devel

BuildRequires:  findutils

Requires:       rpm


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.


%prep
%setup -q -n cmake-%{version}
%patch0 -p1

find . -name *.orig|xargs rm -rf
%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

./bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
            --docdir=/share/doc/%{name}-%{version} --mandir=/share/man \
            --system-libs --no-system-libarchive --no-system-jsoncpp \
            --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN`

make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
#cp -a Example $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/
install -m 0644 Auxiliary/cmake-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

# RPM macros
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake
%{_datadir}/doc/%{name}-%{version}/
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/%{name}/
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*.el
%{_datadir}/aclocal/cmake.m4

%changelog
* Mon Dec 05 2016 sulit - 3.7.1-1
- upgrade cmake to 3.7.1

* Wed Sep 07 2016 sulit <sulitsrc@gmail.com> - 3.6.1-1
- upgrade cmake to 3.6.1

* Tue Dec 29 2015 Cjacker <cjacker@foxmail.com> - 3.4.0-3
- Remove orig files

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 3.4.0-2
- Update, drop python ver patch, already upstream

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 3.3.1-3
- Add more python3 version support

* Fri Oct 23 2015 cjacker - 3.3.1-2
- Rebuild for new 4.0 release

* Wed Sep 16 2015 Cjacker <cjacker@foxmail.com>
- update to 3.3.1

* Tue Aug 14 2007 Cjacker <cjacker@gmail.com> - 2.4.7-1
- Update to 2.4.7

