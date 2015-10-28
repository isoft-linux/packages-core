%define debug_package %{nil}

Summary: The GNU Portable Library Tool
Name:    libtool
Version: 2.4.6
Release: 17
License: GPLv2+ and LGPLv2+ and GFDL
Source:  http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz

URL:     http://www.gnu.org/software/libtool/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: help2man
Requires: autoconf >= 2.58, automake >= 1.4, sed
# make sure we can configure all supported langs
BuildRequires: gcc
# /usr/bin/libtool includes paths within gcc's versioned directories
# Libtool must be rebuilt whenever a new upstream gcc is built
# But we did not want libtool depend on gcc, since we can use clang instead.
#Requires: gcc 

%description
GNU Libtool is a set of shell scripts which automatically configure UNIX and
UNIX-like systems to generically build shared libraries. Libtool provides a
consistent, portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, but do not use
the rest of the GNU Autotools (such as GNU Autoconf and GNU Automake), you
should install the libtool package.

The libtool package also includes all files needed to integrate the GNU 
Portable Library Tool (libtool) and the GNU Libtool Dynamic Module Loader
(ltdl) into a package built using the GNU Autotools (including GNU Autoconf
and GNU Automake).

%prep
%setup -n libtool-%{version} -q

%build
#./bootstrap --force

export CC=gcc
export CXX=g++
export F77=gfortran
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
# don't conflict with libtool-1.5, use own directory:
sed -e 's/pkgdatadir="\\${datadir}\/\$PACKAGE"/pkgdatadir="\\${datadir}\/\${PACKAGE}"/' configure > configure.tmp; mv -f configure.tmp configure; chmod a+x configure

./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --mandir=%{_mandir} --infodir=%{_infodir}  --disable-ltdl-install

# build not smp safe:
make #%{?_smp_mflags}

%check
#make check VERBOSE=yes > make_check.log 2>&1 || (cat make_check.log && false)


%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%exclude %{_datadir}/libtool/libltdl
%{_datadir}/libtool
%{_mandir}/*/*

%changelog
* Fri Oct 23 2015 cjacker - 2.4.6-17
- Rebuild for new 4.0 release

