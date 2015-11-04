%global cache /var/cache/man
%global gnulib_ver 20140202

Summary: Tools for searching and reading man pages
Name: man-db
Version: 2.7.4
Release: 2
# GPLv2+ .. man-db
# GPLv3+ .. gnulib
License: GPLv2+ and GPLv3+
Group: System Environment/Base
URL: http://www.nongnu.org/man-db/

Source0: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source1: man-db.crondaily
Source2: man-db.sysconfig
Patch0: 1151558-switch-man-and-root-in-init-systemd-man-db.conf.patch

Obsoletes: man < 2.0
Provides: man = %{version}
Provides: man-pages-reader = %{version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}

Requires: coreutils, grep, groff, gzip, less
BuildRequires: gdbm-devel, gettext, groff, less, libpipeline-devel, zlib-devel
#BuildRequires: po4a

%description
The man-db package includes five tools for browsing man-pages:
man, whatis, apropos, manpath and lexgrog. man formats and displays
manual pages. whatis searches the manual page names. apropos searches the
manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in
manual pages.

%package cron
Summary: Periodic update of man-db cache
Group: System Environment/Base

Requires: %{name} = %{version}-%{release}
Requires: crontabs

BuildArch: noarch

%description cron
This package provides periodic update of man-db cache.

%prep
%autosetup -p1

%build
%configure \
    --with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
    --disable-setuid --with-browser=elinks --with-lzip=lzip \
    --with-override-dir=overrides
make CC="%{__cc} %{optflags}" %{?_smp_mflags} V=1

#%check
#make check

%install
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'

# move the documentation to the relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim man page - part of groff package
rm $RPM_BUILD_ROOT%{_datadir}/man/man1/zsoelim.1

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d -m 0755  $RPM_BUILD_ROOT%{cache}

# install cron script for man-db creation/update
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/man-db.cron

# config for cron script
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -D -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/man-db

# config for tmpfiles.d
install -D -p -m 0644 init/systemd/man-db.conf $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/.

%find_lang %{name}
%find_lang %{name}-gnulib

# stop and disable timer from previous builds
%pre
if [ -e /usr/lib/systemd/system/mandb.timer ]; then
  if test -d /run/systemd; then
	systemctl stop man-db.timer
	systemctl -q disable man-db.timer
  fi
fi

# clear the old cache
%post
%{__rm} -rf %{cache}/*

# update cache
%transfiletriggerin -- %{_mandir}
/usr/bin/mandb -q

# update cache
%transfiletriggerpostun -- %{_mandir}
/usr/bin/mandb -q

%files -f %{name}.lang -f %{name}-gnulib.lang
%{!?_licensedir:%global license %%doc}
%license docs/COPYING
%doc README man-db-manual.txt man-db-manual.ps ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%config(noreplace) /usr/lib/tmpfiles.d/man-db.conf
%{_sbindir}/accessdb
%{_bindir}/man
%{_bindir}/whatis
%{_bindir}/apropos
%{_bindir}/manpath
%{_bindir}/lexgrog
%{_bindir}/catman
%{_bindir}/mandb
%dir %{_libdir}/man-db
%{_libdir}/man-db/*.so
%dir %{_libexecdir}/man-db
%{_libexecdir}/man-db/globbing
%{_libexecdir}/man-db/manconv
%{_libexecdir}/man-db/zsoelim
%attr(2755,root,man) %verify(not mtime) %dir %{cache}
# documentation and translation
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(es)   %{_datadir}/man/es/man*/*
%lang(it)   %{_datadir}/man/it/man*/*

%files cron
%config(noreplace) %{_sysconfdir}/cron.daily/man-db.cron
%config(noreplace) %{_sysconfdir}/sysconfig/man-db

%changelog
* Wed Nov 04 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 2.7.4-2
- rebuilt

* Wed Nov 04 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 2.7.4-1
- init for isoft.
