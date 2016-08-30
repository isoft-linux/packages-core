%global revision 20160827
Summary: Ncurses support utilities
Name: ncurses
Version: 6.0 
Release: 24.%{revision}%{?dist}
License: MIT
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/current/ncurses-%{version}-%{revision}.tgz

Patch8: ncurses-config.patch
Patch9: ncurses-6.0-libs.patch
Patch11: ncurses-urxvt.patch
Patch12: ncurses-6.0-kbs.patch
BuildRequires: gpm-devel pkgconfig

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains support utilities, including a terminfo compiler
tic, a decompiler infocmp, clear, tput, tset, and a termcap conversion
tool captoinfo.

%package libs
Summary: Ncurses libraries
Requires: %{name}-base = %{version}-%{release}
# libs introduced in 5.6-13 
Obsoletes: ncurses < 5.6-13
Conflicts: ncurses < 5.6-13
Obsoletes: libtermcap < 2.0.8-48

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%package base
Summary: Descriptions of common terminals
Obsoletes: termcap < 1:5.5-2
# base introduced in 5.6-13 
Conflicts: ncurses < 5.6-13
# /lib -> /usr/lib move
Conflicts: filesystem < 3
BuildArch: noarch

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

%package term
Summary: Terminal descriptions
Requires: %{name}-base = %{version}-%{release}
BuildArch: noarch

%description term
This package contains additional terminal descriptions not found in
the ncurses-base package.

%package devel
Summary: Development files for the ncurses library
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Obsoletes: libtermcap-devel < 2.0.8-48
Provides: libtermcap-devel = 2.0.8-48

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package static
Summary: Static libraries for the ncurses library
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The ncurses-static package includes static libraries of the ncurses library.

%prep
%setup -q -n %{name}-%{version}-%{revision}

%patch8 -p1 -b .config
%patch9 -p1 -b .libs
%patch11 -p1 -b .urxvt
%patch12 -p1 -b .kbs

# this will be in documentation, drop executable bits
cp -p install-sh test
find test -type f | xargs chmod 644

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
%global ncurses_options \\\
    --with-shared --without-ada --with-ospeed=unsigned \\\
    --enable-hard-tabs --enable-xmc-glitch --enable-colorfgbg \\\
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \\\
    --enable-overwrite \\\
    --enable-pc-files \\\
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \\\
    --with-termlib=tinfo \\\
    --with-chtype=long \\\
    --with-cxx-shared \\\
    --with-xterm-kbs=DEL

mkdir narrowc widec
cd narrowc
ln -s ../configure .
%configure %{ncurses_options} --with-ticlib
make %{?_smp_mflags} libs
make %{?_smp_mflags} -C progs

cd ../widec
ln -s ../configure .
%configure %{ncurses_options} --enable-widec --without-progs
make %{?_smp_mflags} libs
cd ..

%install
make -C narrowc DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data}
rm -f $RPM_BUILD_ROOT%{_libdir}/libtinfo.*
make -C widec DESTDIR=$RPM_BUILD_ROOT install.{libs,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
for termname in \
    ansi dumb linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    konsole konsole-256color mach\* mlterm mrxvt nsterm putty\* pcansi \
    rxvt{,-\*} screen{,-\*color,.\*} st{,-\*} sun teraterm teraterm2.3 \
    vte vte-256color vwmterm wsvt25\* xfce xterm xterm-\*
do
    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*_g.pc

bzip2 NEWS

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc ANNOUNCE AUTHORS NEWS.bz2 README TO-DO
%{_bindir}/[cirt]*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%{_libdir}/lib*.so.*

%files base -f terms.base
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%dir %{_datadir}/terminfo

%files term -f terms.term

%files devel
%doc test
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc c++/README*
%doc misc/ncurses.supp
%{_bindir}/ncurses*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/ncurses
%dir %{_includedir}/ncursesw
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man3/*

%files static
%{_libdir}/lib*.a

%changelog
* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 6.0-24.20160827
- update ncurses to 6.0-20160827

* Fri Oct 23 2015 cjacker - 6.0-22.20150808
- Rebuild for new 4.0 release

* Mon Aug 10 2015 Cjacker <cjacker@foxmail.com>
- update to 6.0
