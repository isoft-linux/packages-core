Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: 2.3.0
Release: 2
License: (Ruby or BSD) and Public Domain
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/2.2/%{name}-%{version}.tar.bz2

 
BuildRequires: autoconf
BuildRequires: ncurses-devel
BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: gmp-devel
BuildRequires: tcl-devel tk-devel
BuildRequires: gdbm-devel

#avoid any chance link to system ruby library.
BuildConflicts: ruby-devel

Provides: /usr/bin/ruby

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package devel
Summary:    A Ruby development environment
Requires:   %{name} = %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release} 
BuildArch:  noarch

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer -fno-strict-aliasing"
# the configure script does not detect isnan/isinf as macros
export ac_cv_func_isnan=yes
export ac_cv_func_isinf=yes

%configure \
        --disable-rpath \
        --enable-shared \
	--with-ruby-pc=ruby.pc

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
make DESTDIR=%{buildroot} install-doc install-capi

%check
#DISABLE_TESTS=""
#
#%ifarch armv7l armv7hl armv7hnl
## test_call_double(DL::TestDL) fails on ARM HardFP
## http://bugs.ruby-lang.org/issues/6592
#DISABLE_TESTS="-x test_dl2.rb $DISABLE_TESTS"
#%endif
#
## test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
## when abrt.rb cannot be required (seems to be easier way then customizing
## the test suite).
#touch abrt.rb
#make check TESTS="-v $DISABLE_TESTS"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_libdir}/ruby
%{_libdir}/ruby/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libruby-static.a
%{_libdir}/libruby.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root)
%{_docdir}/*
%dir %{_datadir}/ri
%{_datadir}/ri/*

%changelog
* Sat Dec 26 2015 Cjacker <cjacker@foxmail.com> - 2.3.0-2
- Update to 2.3.0

* Fri Oct 23 2015 cjacker - 2.2.3-4
- Rebuild for new 4.0 release

* Mon Sep 07 2015 Cjacker <cjacker@foxmail.com>
- rename ruby-<version>.pc to ruby.pc

* Fri Aug 21 2015 Cjacker <cjacker@foxmail.com>
- update to 2.2.3

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to 2.2.2
- CVE-2015-1855

* Fri Dec 20 2013 Cjacker <cjacker@gmail.com>
- update to 2.0.0-353
