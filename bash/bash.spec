%define baseversion 4.3

Name: bash
Version: %{baseversion}
Summary: The GNU Bourne Again shell
Release: 31 
License: GPLv3+
Url: http://www.gnu.org/software/bash

Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{baseversion}.tar.gz

Source1: dot-bashrc
Source2: dot-bash_profile
Source3: dot-bash_logout

# Official upstream patches
Patch001: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-001
Patch002: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-002
Patch003: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-003
Patch004: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-004
Patch005: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-005
Patch006: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-006
Patch007: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-007
Patch008: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-008
Patch009: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-009
Patch010: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-010
Patch011: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-011
Patch012: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-012
Patch013: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-013
Patch014: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-014
Patch015: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-015
Patch016: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-016
Patch017: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-017
Patch018: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-018
Patch019: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-019
Patch020: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-020
Patch021: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-021
Patch022: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-022
Patch023: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-023
Patch024: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-024
Patch025: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-025
Patch026: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-026
Patch027: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-027
Patch028: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-028
Patch029: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-029
Patch030: ftp://ftp.gnu.org/pub/gnu/bash/bash-4.3-patches/bash43-030

Patch101: privmode-setuid-fail.patch


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

%patch101 -p0


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

rm -rf  $RPM_BUILD_ROOT%{_docdir}/bash
rm -rf  $RPM_BUILD_ROOT%{_infodir}

%find_lang bash

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files -f bash.lang
%defattr(-,root,root)
%config(noreplace) /etc/skel/.b*
%{_bindir}/sh
%{_bindir}/bash
%attr(0755,root,root) %{_bindir}/bashbug-*
%{_mandir}/man1/*

%changelog
* Fri Oct 23 2015 cjacker - 4.3-31
- Rebuild for new 4.0 release

