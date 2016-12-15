Summary: A GNU source-level debugger for C, C++, Java and other languages
Name: gdb
Version: 7.12
Release: 1
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ and GPLv2+ with exceptions and GPL+ and LGPLv2+ and GFDL and BSD and Public Domain
URL: http://gnu.org/software/gdb/
Source0: ftp://sourceware.org/pub/gdb/releases/gdb-%{version}.tar.xz

Source1: gdbinit

BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: expat-devel
BuildRequires: xz-devel
BuildRequires: texinfo gettext flex bison
BuildRequires: python-devel
BuildRequires: libstdc++-devel
BuildRequires: guile-devel
BuildRequires: sharutils dejagnu
BuildRequires: gcc
BuildRequires: gcc-go
BuildRequires: glibc-devel
BuildRequires: libgo
BuildRequires: valgrind
BuildRequires: xz
BuildRequires: zlib-devel
BuildRequires: librpm-devel

Requires: zlib
Requires: readline

%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%prep
%setup -q 
#%patch0 -p1

%build
rm -rf build-%{_target_platform}
mkdir build-%{_target_platform}
cd build-%{_target_platform}

export CFLAGS="$RPM_OPT_FLAGS"
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-system-gdbinit=%{_sysconfdir}/gdbinit \
    --with-gdb-datadir=%{_datadir}/gdb \
    --enable-gdb-build-warnings=,-Wno-unused \
    --with-separate-debug-dir=/usr/lib/debug \
    --enable-gdbserver \
    --with-lzma \
    --with-rpm=librpm.so.7 \
    --enable-inprocess-agent \
    --disable-werror \
    --disable-sim \
    --disable-rpath \
    --with-expat \
    --without-libexpat-prefix \
    --enable-tui \
    --with-python \
    --without-libunwind \
    --enable-64-bit-bfd	\
    --with-auto-load-dir='$debugdir:$datadir/auto-load:%{_datadir}/gdb/auto-load' \
    --with-auto-load-safe-path='$debugdir:$datadir/auto-load:%{_datadir}/gdb/auto-load:%{_bindir}/mono-gdb.py' \
    %{_target_platform}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

pushd build-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

#gdb init setup
#own this dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
touch -r %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
sed 's#%%{_sysconfdir}#%{_sysconfdir}#g' <%{SOURCE1} >$RPM_BUILD_ROOT%{_sysconfdir}/gdbinit
touch -r %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit


#remove unshiped files.
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/lib{bfd*,opcodes*,iberty*,mmalloc*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/gdbinit
%{_sysconfdir}/gdbinit.d
%{_bindir}/gdb
%{_bindir}/gcore
%{_datadir}/gdb
%{_bindir}/gdbserver
%{_libdir}/libinproctrace.so
%{_mandir}/man1/gcore.1*
%{_mandir}/man1/gdb.1*
%{_mandir}/man1/gdbserver.1*
%{_mandir}/man5/gdbinit.5*


%changelog
* Thu Dec 15 2016 sulit - 7.12-1
- upgrade gdb to 7.12

* Fri Oct 23 2015 cjacker - 7.10-2
- Rebuild for new 4.0 release

* Sun Aug 30 2015 Cjacker <cjacker@foxmail.com>
- update to 7.10

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

