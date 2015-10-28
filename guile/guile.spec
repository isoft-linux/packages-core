%define unistring_ver 0.9.3

Summary: A GNU implementation of Scheme for application extensibility
Name: guile
%define mver 2.0
Version: 2.0.11
Release: 2 
Source: ftp://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
Source10: libunistring-%{unistring_ver}.tar.gz

URL: http://www.gnu.org/software/guile/
License: GPLv2+ and LGPLv2+ and GFDL and OFSFDL
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool libltdl-devel gmp-devel readline-devel
BuildRequires: gettext-devel
BuildRequires: gc-devel

#%{?with_emacs:BuildRequires: emacs}
Requires: coreutils
Epoch: 5

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the guile package if you'd like to add extensibility to programs
that you are developing.

%package devel
Summary: Libraries and header files for the GUILE extensibility library
Requires: guile = %{epoch}:%{version}-%{release} gmp-devel gc-devel
Requires: pkgconfig

%description devel
The guile-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the guile-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to
install the guile package.

%prep
%setup -q -n guile-%{version} -a10

%build
pushd libunistring-%{unistring_ver}
CFLAGS="-fPIC" ./configure --prefix=`pwd`/../inter-bin --disable-shared --enable-static
make %{?_smp_mflags}
make install
popd

export PKG_CONFIG_PATH=`pwd`/inter-bin/lib/pkgconfig
%configure \
    --disable-static \
    --disable-error-on-warning \
    --with-libunistring-prefix=`pwd`/inter-bin

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/guile/site

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libguile*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.scm
rm -rf ${RPM_BUILD_ROOT}%{_infodir}

sed -i "s|-L`pwd`/inter-bin/lib||g" ${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig/guile-2.0.pc
sed -i "s|-I`pwd`/inter-bin/include||g" ${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig/guile-2.0.pc
sed -i "s|`pwd`/inter-bin/lib/libunistring.a||g" ${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig/guile-2.0.pc

touch $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slibcat
ln -s ../../slib $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slib

%check
make %{?_smp_mflags} check ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/guile
%{_bindir}/guild
%{_bindir}/guile-tools
%{_libdir}/libguile*.so.*
%{_libdir}/libguilereadline-*.so
%dir %{_libdir}/guile
%{_libdir}/guile/*

%dir %{_datadir}/guile
%dir %{_datadir}/guile/%{mver}
%{_datadir}/guile/%{mver}/*
%ghost %{_datadir}/guile/%{mver}/slibcat
%ghost %{_datadir}/guile/%{mver}/slib
%dir %{_datadir}/guile/site
%{_mandir}/man1/guile.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/guile-config
%{_bindir}/guile-snarf
%{_datadir}/aclocal/*
%{_libdir}/libguile*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/guile


%changelog
* Fri Oct 23 2015 cjacker - 5:2.0.11-2
- Rebuild for new 4.0 release

