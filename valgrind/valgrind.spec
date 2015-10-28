Summary: Tool for finding memory management bugs in programs
Name: valgrind
Version: 3.10.1
Release: 2.svn20150713
Epoch: 1
#Source0: http://www.valgrind.org/downloads/valgrind-%{version}.tar.bz2
#svn co svn://svn.valgrind.org/valgrind/trunk valgrind
Source0: valgrind.tar.gz
Patch0: valgrind-add-glibc-2.21.patch

License: GPLv2
URL: http://www.valgrind.org/
BuildRequires: glibc-devel

# Disable build root strip policy
%define __spec_install_post /usr/lib/rpm/brp-compress || :

# Disable -debuginfo package generation
%define debug_package	%{nil}

%description
Valgrind is a tool to help you find memory-management problems in your
programs. When a program is run under Valgrind's supervision, all
reads and writes of memory are checked, and calls to
malloc/new/free/delete are intercepted. As a result, Valgrind can
detect a lot of problems that are otherwise very hard to
find/diagnose.

%package devel
Summary: Development files for valgrind
Requires: valgrind = %{epoch}:%{version}-%{release}

%description devel
Header files and libraries for development of valgrind aware programs
or valgrind plugins.

%prep
%setup -q -n %{name}
#%patch0 -p1
#%patch2 -p1

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi 
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

#do not strip /usr/lib/valgrind/*
#pushd $RPM_BUILD_ROOT/%{_bindir}
#strip --strip-debug * || echo
#popd

%check 
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*[^ao]
%{_libdir}/valgrind/[^l]*o
#%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/valgrind
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*.a
%{_libdir}/pkgconfig/*

%changelog
* Fri Oct 23 2015 cjacker - 1:3.10.1-2.svn20150713
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

