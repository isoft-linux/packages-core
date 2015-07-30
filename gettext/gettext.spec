Summary: GNU libraries and utilities for producing multi-lingual messages
Name: gettext
Version: 0.19.4
Release: 1 
License: GPLv3 and LGPLv2+
Group: Core/Development/Utility
URL: http://www.gnu.org/software/gettext/
Source: ftp://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
Source2: msghack.py
%ifarch x86_64 ppc64 s390x
BuildRequires: automake >= 1.8
%endif
BuildRequires: autoconf >= 2.5
BuildRequires: libtool, bison

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.


%package devel
Summary: Development files for %{name}
Group:  Core/Development/Library
License: LGPLv2+
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.


%package libs
Summary: Libraries for %{name}
Group:  Core/Runtime/Library
License: LGPLv2+

%description libs
This package contains libraries used internationalization support.


%prep
%setup -q 

%build

[ -f  %{_datadir}/automake/depcomp ] && cp -f %{_datadir}/automake/{depcomp,ylwrap} .

%configure \
    --disable-static \
    --enable-shared \
    --with-pic-=yes \
    --disable-csharp \
    --disable-java \
    --with-included-libcroco \
    --with-included-libunistring \
    --disable-openmp \
    --with-included-glib \
    --with-included-libxml \
    --without-included-gettext \
    --enable-nls \
    --disable-rpath

make %{?_smp_mflags}

%check
make check

%install
rm -rf %{buildroot}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="%{__install} -p" \
    lispdir=%{_datadir}/emacs/site-lisp \
    aclocaldir=%{_datadir}/aclocal EXAMPLESFILES=""

install -pm 755 %SOURCE2 ${RPM_BUILD_ROOT}/%{_bindir}/msghack

# make preloadable_libintl.so executable
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/preloadable_libintl.so

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# doc relocations
for i in gettext-runtime/man/*.html; do
  rm ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/`basename $i`
done
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/javadoc*

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/* ${RPM_BUILD_ROOT}/%{_datadir}/doc/libasprintf/* htmldoc
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext

# remove unpackaged files from the buildroot
##rm -rf ${RPM_BUILD_ROOT}%{_datadir}/emacs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

%find_lang %{name}-runtime
%find_lang %{name}-tools
cat %{name}-*.lang > %{name}.lang


# rename start-po.el to site-start.d/po-mode-init.el
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}/*.class
rpmclean

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig



%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/libgettextlib-*.so
%{_libdir}/libgettextsrc-*.so
%{_mandir}/man1/*
%{_libdir}/%{name}
#%exclude %{_libdir}/%{name}/gnu.gettext.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/styles
%{_datadir}/gettext/archive.dir.tar.xz

%files devel
%defattr(-,root,root,-)
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/projects/
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/aclocal/*
%{_includedir}/*
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextsrc.so
%{_libdir}/preloadable_libintl.so
%{_mandir}/man3/*
#%{_libdir}/%{name}/gnu.gettext.*


%files libs
%defattr(-,root,root,-)
%{_libdir}/libasprintf.so.*
%{_libdir}/libgettextpo.so.*

