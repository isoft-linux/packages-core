%ifarch x86_64
%global archs %{ix86} x86_64
%else
%ifarch %{ix86}
%global archs %{ix86}
%else
%global archs %{_target_cpu}
%endif
%endif

%define abs2rel() perl -MFile::Spec -e 'print File::Spec->abs2rel(@ARGV)' %1 %2
%global relccache %(%abs2rel %{_bindir}/ccache %{_libdir}/ccache)

Name:           ccache
Version:        3.2.2
Release:        2%{?dist}
Summary:        C/C++ compiler cache

Group:          Development/Tools
License:        GPLv3+
URL:            http://ccache.samba.org/
Source0:        http://samba.org/ftp/ccache/%{name}-%{version}.tar.xz
Source1:        %{name}.sh.in
Source2:        %{name}.csh.in
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(File::Spec)
BuildRequires:  zlib-devel >= 1.2.3
# coreutils for triggerin, triggerpostun
Requires:       coreutils

%description
ccache is a compiler cache.  It speeds up recompilation of C/C++ code
by caching previous compiles and detecting when the same compile is
being done again.  The main focus is to handle the GNU C/C++ compiler
(GCC), but it may also work with compilers that mimic GCC good enough.


%prep
%setup -q
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE1} > %{name}.sh
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE2} > %{name}.csh
# Make sure system zlib is used
rm -r zlib


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{name}.sh %{name}.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

install -dm 770 $RPM_BUILD_ROOT%{_var}/cache/ccache

# %%ghost files for ownership, keep in sync with triggers
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/ccache
for n in cc gcc g++ c++ ; do
    ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n
    for p in avr arm-gp2x-linux arm-none-eabi msp430 ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$p-$n
    done
    for p in aarch64 alpha arm avr32 bfin c6x cris frv h8300 hppa hppa64 ia64 m32r \
        m68k microblaze mips64 mn10300 nios2 powerpc64 ppc64 s390x sh sh64 sparc64 \
        tile x86_64 xtensa ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$p-linux-gnu-$n
    done
    for s in 32 34 4 44 ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n$s
    done
    for a in %{archs} ; do
        ln -s %{relccache} \
            $RPM_BUILD_ROOT%{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n
    done
done
for n in clang clang++ ; do
    ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n
done
find $RPM_BUILD_ROOT%{_libdir}/ccache -type l | \
    sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" > %{name}-%{version}.compilers


%check
make check


%clean
rm -fr $RPM_BUILD_ROOT


%define ccache_trigger(p:) \
%triggerin -- %{-p*}\
for n in %* ; do\
    [ ! -x %{_bindir}/$n ] || ln -sf %{relccache} %{_libdir}/ccache/$n\
    for a in %{archs} ; do\
        [ ! -x %{_bindir}/$a-%{_vendor}-%{_target_os}-$n ] || \\\
          ln -sf %{relccache} %{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n\
    done\
done\
:\
%triggerpostun -- %{-p*}\
for n in %* ; do\
    [ -x %{_bindir}/$n ] || rm -f %{_libdir}/ccache/$n\
    for a in %{archs} ; do\
        [ -x %{_bindir}/$a-%{_vendor}-%{_target_os}-$n ] || \\\
            rm -f %{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n\
    done\
done\
:\
%{nil}

%ccache_trigger -p arm-gp2x-linux-gcc arm-gp2x-linux-cc arm-gp2x-linux-gcc
%ccache_trigger -p arm-gp2x-linux-gcc-c++ arm-gp2x-linux-c++ arm-gp2x-linux-g++
%ccache_trigger -p arm-none-eabi-gcc-cs arm-none-eabi-gcc
%ccache_trigger -p avr-gcc avr-cc avr-gcc
%ccache_trigger -p avr-gcc-c++ avr-c++ avr-g++
%ccache_trigger -p clang clang clang++
%ccache_trigger -p compat-gcc-32 cc32 gcc32
%ccache_trigger -p compat-gcc-32-c++ c++32 g++32
%ccache_trigger -p compat-gcc-34 cc34 gcc34
%ccache_trigger -p compat-gcc-34-c++ c++34 g++34
#we have only one gcc package 
%ccache_trigger -p gcc cc gcc c++ g++
%ccache_trigger -p gcc-c++ c++ g++
%ccache_trigger -p gcc4 cc4 gcc4
%ccache_trigger -p gcc4-c++ c++4 g++4
%ccache_trigger -p gcc44 cc4 gcc44
%ccache_trigger -p gcc44-c++ c++44 g++44
%ccache_trigger -p mingw32-gcc i686-pc-mingw32-cc i686-pc-mingw32-gcc i686-w64-mingw32-gcc
%ccache_trigger -p mingw32-gcc-c++ i686-pc-mingw32-c++ i686-pc-mingw32-g++ i686-w64-mingw32-c++ i686-w64-mingw32-g++
%ccache_trigger -p mingw64-gcc i686-w64-mingw32-gcc x86_64-w64-mingw32-gcc
%ccache_trigger -p mingw64-gcc-c++ i686-w64-mingw32-c++ i686-w64-mingw32-g++ x86_64-w64-mingw32-c++ x86_64-w64-mingw32-g++
%ccache_trigger -p msp430-gcc msp430-cc msp430-gcc
# cross-gcc
%ccache_trigger -p gcc-aarch64-linux-gnu aarch64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-aarch64-linux-gnu aarch64-linux-gnu-c++ aarch64-linux-gnu-g++
%ccache_trigger -p gcc-alpha-linux-gnu alpha-linux-gnu-gcc
%ccache_trigger -p gcc-c++-alpha-linux-gnu alpha-linux-gnu-c++ alpha-linux-gnu-g++
%ccache_trigger -p gcc-arm-linux-gnu arm-linux-gnu-gcc
%ccache_trigger -p gcc-c++-arm-linux-gnu arm-linux-gnu-c++ arm-linux-gnu-g++
%ccache_trigger -p gcc-avr32-linux-gnu avr32-linux-gnu-gcc
%ccache_trigger -p gcc-c++-avr32-linux-gnu avr32-linux-gnu-c++ avr32-linux-gnu-g++
%ccache_trigger -p gcc-bfin-linux-gnu bfin-linux-gnu-gcc
%ccache_trigger -p gcc-c++-bfin-linux-gnu bfin-linux-gnu-c++ bfin-linux-gnu-g++
%ccache_trigger -p gcc-c6x-linux-gnu c6x-linux-gnu-gcc
%ccache_trigger -p gcc-c++-c6x-linux-gnu c6x-linux-gnu-c++ c6x-linux-gnu-g++
%ccache_trigger -p gcc-cris-linux-gnu cris-linux-gnu-gcc
%ccache_trigger -p gcc-c++-cris-linux-gnu cris-linux-gnu-c++ cris-linux-gnu-g++
%ccache_trigger -p gcc-frv-linux-gnu frv-linux-gnu-gcc
%ccache_trigger -p gcc-c++-frv-linux-gnu frv-linux-gnu-c++ frv-linux-gnu-g++
%ccache_trigger -p gcc-h8300-linux-gnu h8300-linux-gnu-gcc
%ccache_trigger -p gcc-hppa-linux-gnu hppa-linux-gnu-gcc
%ccache_trigger -p gcc-c++-hppa-linux-gnu hppa-linux-gnu-c++ hppa-linux-gnu-g++
%ccache_trigger -p gcc-hppa64-linux-gnu hppa64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-hppa64-linux-gnu hppa64-linux-gnu-c++ hppa64-linux-gnu-g++
%ccache_trigger -p gcc-ia64-linux-gnu ia64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-ia64-linux-gnu ia64-linux-gnu-c++ ia64-linux-gnu-g++
%ccache_trigger -p gcc-m32r-linux-gnu m32r-linux-gnu-gcc
%ccache_trigger -p gcc-c++-m32r-linux-gnu m32r-linux-gnu-c++ m32r-linux-gnu-g++
%ccache_trigger -p gcc-m68k-linux-gnu m68k-linux-gnu-gcc
%ccache_trigger -p gcc-c++-m68k-linux-gnu m68k-linux-gnu-c++ m68k-linux-gnu-g++
%ccache_trigger -p gcc-microblaze-linux-gnu microblaze-linux-gnu-gcc
%ccache_trigger -p gcc-c++-microblaze-linux-gnu microblaze-linux-gnu-c++ microblaze-linux-gnu-g++
%ccache_trigger -p gcc-mips64-linux-gnu mips64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-mips64-linux-gnu mips64-linux-gnu-c++ mips64-linux-gnu-g++
%ccache_trigger -p gcc-mn10300-linux-gnu mn10300-linux-gnu-gcc
%ccache_trigger -p gcc-c++-mn10300-linux-gnu mn10300-linux-gnu-c++ mn10300-linux-gnu-g++
%ccache_trigger -p gcc-nios2-linux-gnu nios2-linux-gnu-gcc
%ccache_trigger -p gcc-c++-nios2-linux-gnu nios2-linux-gnu-c++ nios2-linux-gnu-g++
%ccache_trigger -p gcc-powerpc64-linux-gnu powerpc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-powerpc64-linux-gnu powerpc64-linux-gnu-c++ powerpc64-linux-gnu-g++
%ccache_trigger -p gcc-ppc64-linux-gnu ppc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-ppc64-linux-gnu ppc64-linux-gnu-c++ ppc64-linux-gnu-g++
%ccache_trigger -p gcc-s390x-linux-gnu s390x-linux-gnu-gcc
%ccache_trigger -p gcc-c++-s390x-linux-gnu s390x-linux-gnu-c++ s390x-linux-gnu-g++
%ccache_trigger -p gcc-sh-linux-gnu sh-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sh-linux-gnu sh-linux-gnu-c++ sh-linux-gnu-g++
%ccache_trigger -p gcc-sh64-linux-gnu sh64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sh64-linux-gnu sh64-linux-gnu-c++ sh64-linux-gnu-g++
%ccache_trigger -p gcc-sparc64-linux-gnu sparc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sparc64-linux-gnu sparc64-linux-gnu-c++ sparc64-linux-gnu-g++
%ccache_trigger -p gcc-tile-linux-gnu tile-linux-gnu-gcc
%ccache_trigger -p gcc-c++-tile-linux-gnu tile-linux-gnu-c++ tile-linux-gnu-g++
%ccache_trigger -p gcc-x86_64-linux-gnu x86_64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-x86_64-linux-gnu x86_64-linux-gnu-c++ x86_64-linux-gnu-g++
%ccache_trigger -p gcc-xtensa-linux-gnu xtensa-linux-gnu-gcc
%ccache_trigger -p gcc-c++-xtensa-linux-gnu xtensa-linux-gnu-c++ xtensa-linux-gnu-g++

%pre
getent group ccache >/dev/null || groupadd -r ccache || :


%files -f %{name}-%{version}.compilers
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license GPL-3.0.txt LICENSE.*
%doc AUTHORS.*  MANUAL.* NEWS.* README.*
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_bindir}/ccache
%dir %{_libdir}/ccache/
%attr(2770,root,ccache) %dir %{_var}/cache/ccache/
%{_mandir}/man1/ccache.1*


%changelog
