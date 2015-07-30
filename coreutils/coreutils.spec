Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.23
Release: 1
License: GPLv3+
Group:   Core/Runtime/Utility
Url:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source101:  coreutils-DIR_COLORS
Source102:  coreutils-DIR_COLORS.lightbgcolor
Source103:  coreutils-DIR_COLORS.256color
Source105:  coreutils-colorls.sh
Source106:  coreutils-colorls.csh


Conflicts: filesystem < 3
Provides: /bin/basename
Provides: /bin/cat
Provides: /bin/chgrp
Provides: /bin/chmod
Provides: /bin/chown
Provides: /bin/cp
Provides: /bin/cut
Provides: /bin/date
Provides: /bin/dd
Provides: /bin/df
Provides: /bin/echo
Provides: /bin/env
Provides: /bin/false
Provides: /bin/ln
Provides: /bin/ls
Provides: /bin/mkdir
Provides: /bin/mknod
Provides: /bin/mktemp
Provides: /bin/mv
Provides: /bin/nice
Provides: /bin/pwd
Provides: /bin/readlink
Provides: /bin/rm
Provides: /bin/rmdir
Provides: /bin/sleep
Provides: /bin/sort
Provides: /bin/stty
Provides: /bin/sync
Provides: /bin/touch
Provides: /bin/true
Provides: /bin/uname

BuildRequires: libacl-devel
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: attr

Requires:       ncurses

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
#old mktemp package had epoch 3, so we have to use 4 for coreutils
Provides: mktemp = 4:%{version}-%{release}

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%prep
%setup -q

%build
export FORCE_UNSAFE_CONFIGURE=1
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpic"
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
%configure --enable-largefile \
            --without-gmp \
            --enable-no-install-program=su,kill,uptime \
            --disable-libcap \
            --with-tty-group \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :

make all 
#smp build broken
#%{?_smp_mflags}

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

%install
rm -rf $RPM_BUILD_ROOT
#to avoid "makeinfo" not found.
make DESTDIR=$RPM_BUILD_ROOT install

# man pages are not installed with make install
make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT{%_bindir,%_sbindir}

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT{%_bindir,%_sbindir}/chroot

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 %SOURCE101 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS
install -p -c -m644 %SOURCE102 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.lightbgcolor
install -p -c -m644 %SOURCE103 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.256color
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

# Compress ChangeLogs from before the fileutils/textutils/etc merge
bzip2 -f9 old/*/C*

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)


rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
#failed, test-getaddrinfo need network
make check||:

%postun
if [ -x /usr/bin/busybox ]; then
/usr/bin/busybox --install -s
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/coreutils*
%{_mandir}/man*/*
%{_datadir}/locale/*

%changelog
