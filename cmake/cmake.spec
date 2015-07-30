Name:		cmake
Version:    3.3.0	
Release:	1
Summary:	Cross-platform make system

Group:		CoreDev/Development/Utility
License:	BSD
URL:		http://www.cmake.org
Source0:	http://www.cmake.org/files/v2.4/cmake-%{version}-rc2.tar.gz
Source2:        macros.cmake
Source3: 	    cmake-init.el
Patch0:         cmake-set-lib-to-usr_lib.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ncurses-devel
BuildRequires:  expat-devel, zlib-devel, libcurl-devel
#BuildRequires:  libarchive-devel
Requires:       rpm


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.


%prep
%setup -q -n cmake-%{version}-rc2
%patch0 -p1
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

rpmclean

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
#%{_mandir}/man1/*.1*
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/emacs/site-lisp/site-start.d/*.el
%{_datadir}/aclocal/cmake.m4

%changelog
* Tue Aug 14 2007 Cjacker <cjacker@gmail.com> - 2.4.7-1
- Update to 2.4.7

