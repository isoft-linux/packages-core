%global revision 20150214
Summary: Ncurses support utilities
Name:    ncurses
Version: 5.9
Release: 1 
License: MIT
Group:   Core/Runtime/Utility 
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/current/ncurses-%{version}-%{revision}.tgz

Patch8: ncurses-config.patch
Patch9: ncurses-libs.patch
Patch11: ncurses-urxvt.patch
Patch12: ncurses-kbs.patch

Requires: %{name}-libs = %{version}-%{release}

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
Group:  Core/Runtime/Library 
Requires: %{name}-base = %{version}-%{release}

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%package base
Summary: Descriptions of common terminals
Group:   Core/Runtime/Data

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

%package devel
Summary: Development files for the ncurses library
Group:   Core/Development/Library 
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package static
Summary: Static libraries for the ncurses library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The ncurses-static package includes static libraries of the ncurses library.

%prep
%setup -q -n ncurses-%{version}-%{revision}
%patch8 -p1 -b .config
%patch9 -p1 -b .libs
%patch11 -p1 -b .urxvt
%patch12 -p1 -b .kbs

%build

mkdir narrowc widec
cd narrowc
ln -s ../configure .
%configure --without-ada \
        --disable-termcap \
        --disable-rpath-hack \
        --without-cxx-binding \
        --with-termlib=tinfo    \
        --enable-hard-tabs \
        --enable-xmc-glitch \
        --with-ticlib \
        --enable-colorfgbg \
        --with-terminfo-dirs="/etc/terminfo:/usr/share/terminfo" \
        --enable-pc-files \
        --with-pkg-config-libdir="/usr/lib/pkgconfig" \
        --with-shared
make %{?_smp_mflags} libs
make %{?_smp_mflags} -C progs

cd ../widec
ln -s ../configure .
%configure --without-ada \
        --disable-termcap \
        --disable-rpath-hack \
        --without-cxx-binding \
        --with-termlib=tinfo    \
        --enable-hard-tabs \
        --enable-xmc-glitch \
        --enable-colorfgbg \
        --with-terminfo-dirs="/etc/terminfo:/usr/share/terminfo" \
        --enable-pc-files \
        --with-pkg-config-libdir="/usr/lib/pkgconfig" \
        --with-shared \
        --enable-widec \
        --without-progs
make %{?_smp_mflags} libs
cd ..

%install
rm -rf ${RPM_BUILD_ROOT}

make -C narrowc DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data}
rm -f $RPM_BUILD_ROOT%{_libdir}/libtinfo.*
make -C widec DESTDIR=$RPM_BUILD_ROOT install.{libs,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

for i in ansi console dumb linux rxvt screen sun vt52 vt100 vt102 \
        vt200 vt220 xterm xterm-color xterm-xfree86; do
    termfile=$(find $RPM_BUILD_ROOT/usr/share/terminfo/ -name "$i" 2>/dev/null)
    basedir=$(basename $(dirname "$termfile"))

    [ -z "$termfile" ] && continue

    install -d $RPM_BUILD_ROOT/etc/terminfo/$basedir
    mv ${termfile} $RPM_BUILD_ROOT/etc/terminfo/$basedir/
    ln -s ../../../../etc/terminfo/$basedir/$i \
        $RPM_BUILD_ROOT/usr/share/terminfo/$basedir/$i
done


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
#rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/{*_g,ncurses++*}.pc

rpmclean

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/[cirt]*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files base 
%defattr(-,root,root)
%dir %{_sysconfdir}/terminfo
%{_sysconfdir}/terminfo/*
%{_datadir}/tabset
%dir %{_datadir}/terminfo
%{_datadir}/terminfo/*

%files devel
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_libdir}/lib*.a

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
