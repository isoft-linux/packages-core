%global patch_level 353

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: 2.1.1
Release: 2
#.p%{patch_level}
Group: CoreDev/Development/Language
License: (Ruby or BSD) and Public Domain
URL: http://ruby-lang.org/
Source0: ftp://ftp.ruby-lang.org/pub/%{name}/2.0/%{name}-%{version}.tar.gz
#Source0: ftp://ftp.ruby-lang.org/pub/%{name}/2.0/%{name}-%{version}-p%{patch_level}.tar.gz
Patch0:   ruby-test_exception-segfault.patch 
Patch3:   ruby-with-libressl.patch
 
BuildRequires: autoconf
BuildRequires: ncurses-devel
BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
Provides: /usr/bin/ruby

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package devel
Summary:    A Ruby development environment
Group:      CoreDev/Development/Library
Requires:   %{name} = %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package doc
Summary:    Documentation for %{name}
Group:      CoreDev/Development/Document
Requires:   %{name} = %{version}-%{release} 
BuildArch:  noarch

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
#%patch3 -p1

%build
export CFLAGS="$CFLAGS -fno-omit-frame-pointer -fno-strict-aliasing"
# the configure script does not detect isnan/isinf as macros
export ac_cv_func_isnan=yes
export ac_cv_func_isinf=yes

%configure \
        --disable-rpath \
        --enable-shared

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
make DESTDIR=%{buildroot} install-doc install-capi

rpmclean

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
* Fri Dec 20 2013 Cjacker <cjacker@gmail.com>
- update to 2.0.0-353
