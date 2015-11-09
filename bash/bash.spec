%define baseversion 4.3

Name: bash
Version: %{baseversion}
Summary: The GNU Bourne Again shell
Release: 32 
License: GPLv3+
Url: http://www.gnu.org/software/bash

Source0: http://ftp.gnu.org/gnu/bash/bash-%{baseversion}.tar.gz

Source1: dot-bashrc
Source2: dot-bash_profile
Source3: dot-bash_logout

# Official upstream patches
Patch001: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-001
Patch002: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-002
Patch003: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-003
Patch004: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-004
Patch005: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-005
Patch006: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-006
Patch007: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-007
Patch008: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-008
Patch009: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-009
Patch010: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-010
Patch011: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-011
Patch012: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-012
Patch013: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-013
Patch014: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-014
Patch015: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-015
Patch016: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-016
Patch017: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-017
Patch018: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-018
Patch019: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-019
Patch020: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-020
Patch021: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-021
Patch022: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-022
Patch023: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-023
Patch024: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-024
Patch025: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-025
Patch026: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-026
Patch027: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-027
Patch028: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-028
Patch029: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-029
Patch030: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-030
Patch031: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-031
Patch032: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-032
Patch033: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-033
Patch034: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-034
Patch035: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-035
Patch036: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-036
Patch037: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-037
Patch038: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-038
Patch039: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-039
Patch040: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-040
Patch041: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-041
Patch042: http://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-042

# Other patches
Patch101: bash-2.02-security.patch
Patch102: bash-2.03-paths.patch
Patch103: bash-2.03-profile.patch
Patch104: bash-2.05a-interpreter.patch
Patch105: bash-2.05b-debuginfo.patch
Patch106: bash-2.05b-manso.patch
Patch107: bash-2.05b-pgrp_sync.patch
Patch108: bash-2.05b-readline-oom.patch
Patch109: bash-2.05b-xcc.patch
Patch110: bash-3.2-audit.patch
Patch111: bash-3.2-ssh_source_bash.patch
Patch112: bash-bashbug.patch
Patch113: bash-infotags.patch
Patch114: bash-requires.patch
Patch115: bash-setlocale.patch
Patch116: bash-tty-tests.patch

# 484809, check if interp section is NOBITS
Patch117: bash-4.0-nobits.patch

# Do the same CFLAGS in generated Makefile in examples
Patch118: bash-4.1-examples.patch

# Builtins like echo and printf won't report errors
# when output does not succeed due to EPIPE
Patch119: bash-4.1-broken_pipe.patch

# Enable system-wide .bash_logout for login shells
Patch120: bash-4.2-rc2-logout.patch

# Static analyzis shows some issues in bash-2.05a-interpreter.patch
Patch121: bash-4.2-coverity.patch

# Don't call malloc in signal handler
Patch122: bash-4.1-defer-sigchld-trap.patch

# 799958, updated info about trap
Patch123: bash-4.2-manpage_trap.patch

# https://www.securecoding.cert.org/confluence/display/seccode/INT32-C.+Ensure+that+operations+on+signed+integers+do+not+result+in+overflow
Patch125: bash-4.2-size_type.patch

# fix deadlock in trap, backported from devel branch
Patch127: bash-4.2-trap.patch

# 1112710 - mention ulimit -c and -f POSIX block size
Patch128: bash-4.3-man-ulimit.patch

# A series of patches emitted by upstream since 4.3-18
#Patch131: bash-4.3-parse-time-keyword.patch
Patch134: bash-4.3-pathexp-globignore-delim.patch

# 1102815 - fix double echoes in vi visual mode
Patch135: bash-4.3-noecho.patch

# 1182278 - bash crashes on `select' if REPLY is readonly
Patch137: bash-4.3-select-readonly.patch

#1241533,1224855 - bash leaks memory when LC_ALL set
Patch138: bash-4.3-memleak-lc_all.patch

#1245233 - old memleak reappeared, taken from upstream
Patch139: bash-4.3-old-memleak.patch

Patch200: privmode-setuid-fail.patch

BuildRequires: bison flex byacc
BuildRequires: ncurses-devel
BuildRequires: gettext
Provides: /bin/sh
Provides: /bin/bash

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification.

%prep
%setup -q -n %{name}-%{baseversion}

# Official upstream patches
%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0

# Other patches
%patch101 -p1 -b .security
%patch102 -p1 -b .paths
%patch103 -p1 -b .profile
%patch104 -p1 -b .interpreter
%patch105 -p1 -b .debuginfo
%patch106 -p1 -b .manso
%patch107 -p1 -b .pgrp_sync
%patch108 -p1 -b .readline_oom
%patch109 -p1 -b .xcc
%patch110 -p1 -b .audit
%patch111 -p1 -b .ssh_source_bash
%patch112 -p1 -b .bashbug
%patch113 -p1 -b .infotags
%patch114 -p1 -b .requires
%patch115 -p1 -b .setlocale
%patch116 -p1 -b .tty_tests
%patch117 -p1 -b .nobits
%patch118 -p1 -b .examples
%patch119 -p1 -b .broken_pipe
%patch120 -p1 -b .logout
%patch121 -p1 -b .coverity
%patch122 -p1 -b .defer_sigchld_trap
%patch123 -p1
%patch125 -p1 -b .size_type
%patch128 -p1 -b .ulimit
#%patch131 -p0 -b .keyword
%patch134 -p0 -b .delim
%patch135 -p1 -b .noecho
%patch137 -p1 -b .readonly
%patch138 -p1 -b .lc_all
%patch139 -p1 -b .oldleak


%patch200 -p0


echo %{version} > _distribution
echo %{release} > _patchlevel

%build
autoconf
%configure \
    --with-bash-malloc=no \
    --with-curses \
    --enable-readline \
    --enable-cond-regexp
# Recycles pids is neccessary. When bash's last fork's pid was X
# and new fork's pid is also X, bash has to wait for this same pid.
# Without Recycles pids bash will not wait.
make "CPPFLAGS=-D_GNU_SOURCE -DRECYCLES_PIDS `getconf LFS_CFLAGS`"
 
%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/etc

pushd $RPM_BUILD_ROOT
ln -sf bash .%{_bindir}/sh
popd

mkdir -p $RPM_BUILD_ROOT/etc/skel
install -c -m644 %SOURCE1 $RPM_BUILD_ROOT/etc/skel/.bashrc
install -c -m644 %SOURCE2 $RPM_BUILD_ROOT/etc/skel/.bash_profile
install -c -m644 %SOURCE3 $RPM_BUILD_ROOT/etc/skel/.bash_logout

LONG_BIT=$(getconf LONG_BIT)
mv $RPM_BUILD_ROOT%{_bindir}/bashbug \
   $RPM_BUILD_ROOT%{_bindir}/bashbug-"${LONG_BIT}"
ln -s bashbug.1 $RPM_BUILD_ROOT/%{_mandir}/man1/bashbug-"$LONG_BIT".1

# bug #820192, need to add execable alternatives for regular built-ins
for ea in alias bg cd command fc fg getopts jobs read umask unalias wait
do
  cat <<EOF > "$RPM_BUILD_ROOT"/%{_bindir}/"$ea"
#!/bin/sh
builtin $ea "\$@"
EOF
chmod +x "$RPM_BUILD_ROOT"/%{_bindir}/"$ea"
done

rm -rf  $RPM_BUILD_ROOT%{_docdir}/bash
rm -rf  $RPM_BUILD_ROOT%{_infodir}

%find_lang bash

%check
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 make check

%clean
rm -rf $RPM_BUILD_ROOT

%files -f bash.lang
%defattr(-,root,root)
%config(noreplace) /etc/skel/.b*
%{_bindir}/sh
%{_bindir}/bash
%attr(0755,root,root) %{_bindir}/bashbug-*
%{_bindir}/alias
%{_bindir}/bg
%{_bindir}/cd
%{_bindir}/command
%{_bindir}/fc
%{_bindir}/fg
%{_bindir}/getopts
%{_bindir}/jobs
%{_bindir}/read
%{_bindir}/umask
%{_bindir}/unalias
%{_bindir}/wait
%{_mandir}/man1/*

%changelog
* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 4.3-32
- Add patches from upstream(Patch Level 42)

* Fri Oct 23 2015 cjacker - 4.3-31
- Rebuild for new 4.0 release

