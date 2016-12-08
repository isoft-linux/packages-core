Summary: Gives a fake root environment
Name: fakeroot
Version: 1.21
Release: 1%{?dist}
License: GPL+
URL: http://fakeroot.alioth.debian.org/
Source0: http://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.gz
# Address some POSIX-types related problems.
Patch0: fakeroot-inttypes.patch
BuildRequires: /usr/bin/getopt
BuildRequires: libcap-devel
# uudecode used by tests/tartest
BuildRequires: sharutils
BuildRequires: autoconf automake libtool
Requires: /usr/bin/getopt
Requires: fakeroot-libs = %{version}-%{release}
Requires(post): /usr/sbin/alternatives
Requires(post): /usr/bin/readlink
Requires(preun): /usr/sbin/alternatives


%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary: Gives a fake root environment (libraries)

%description libs
This package contains the libraries required by %{name}.

%prep
%setup -q
%patch0 -p1 -b .inttypes
for makefile in ./doc/*/Makefile.am; do
	sed -i -e "s@man_MANS = faked.1 fakeroot.1@man_MANS = ../faked.1 ../fakeroot.1@g" $makefile
	sed -i -e "s@man_MANS = fakeroot.1 faked.1@man_MANS = ../fakeroot.1 ../faked.1@g" $makefile
done

for file in ./doc/*.1; do
  iconv -f latin1 -t utf8 < $file > $file.new
  mv -f $file.new $file
done

%build
./bootstrap
for type in sysv tcp; do
mkdir obj-$type
cd obj-$type
cat >> configure << 'EOF'
#!/bin/sh
exec ../configure "$@"
EOF
chmod +x configure
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --libdir=%{_libdir}/libfakeroot \
  --with-ipc=$type \
  --program-suffix=-$type
make
cd ..
done

%install
for type in sysv tcp; do
  make -C obj-$type install libdir=%{_libdir}/libfakeroot DESTDIR=%{buildroot}
  chmod 644 %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so 
  mv %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so \
     %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  strip -s %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*la
  %find_lang faked-$type --without-mo --with-man
  %find_lang fakeroot-$type --without-mo --with-man
done

cat fake{d,root}-{sysv,tcp}.lang > fakeroot.lang

%check
for type in sysv tcp; do
  make -C obj-$type check
done

%post
link=$(readlink -e "/usr/bin/fakeroot")
if [ "$link" = "/usr/bin/fakeroot" ]; then
  rm -f /usr/bin/fakeroot
fi
link=$(readlink -e "%{_bindir}/faked")
if [ "$link" = "%{_bindir}/faked" ]; then
  rm -f "%{_bindir}/faked"
fi
link=$(readlink -e "%{_libdir}/libfakeroot/libfakeroot-0.so")
if [ "$link" = "%{_libdir}/libfakeroot/libfakeroot-0.so" ]; then
  rm -f "%{_libdir}/libfakeroot/libfakeroot-0.so"
fi

/usr/sbin/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-tcp" 50 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-tcp \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-tcp.so \
  --slave %{_mandir}/man1/fakeroot.1.gz fakeroot.1.gz %{_mandir}/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/man1/faked.1.gz faked.1.gz %{_mandir}/man1/faked-tcp.1.gz \
  --slave %{_mandir}/de/man1/fakeroot.1.gz fakeroot.de.1.gz %{_mandir}/de/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/de/man1/faked.1.gz faked.de.1.gz %{_mandir}/de/man1/faked-tcp.1.gz \
  --slave %{_mandir}/es/man1/fakeroot.1.gz fakeroot.es.1.gz %{_mandir}/es/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/es/man1/faked.1.gz faked.es.1.gz %{_mandir}/es/man1/faked-tcp.1.gz \
  --slave %{_mandir}/fr/man1/fakeroot.1.gz fakeroot.fr.1.gz %{_mandir}/fr/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/fr/man1/faked.1.gz faked.fr.1.gz %{_mandir}/fr/man1/faked-tcp.1.gz \
  --slave %{_mandir}/nl/man1/fakeroot.1.gz fakeroot.nl.1.gz %{_mandir}/nl/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/nl/man1/faked.1.gz faked.nl.1.gz %{_mandir}/nl/man1/faked-tcp.1.gz \
  --slave %{_mandir}/pt/man1/fakeroot.1.gz fakeroot.pt.1.gz %{_mandir}/pt/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/pt/man1/faked.1.gz faked.pt.1.gz %{_mandir}/pt/man1/faked-tcp.1.gz \
  --slave %{_mandir}/sv/man1/fakeroot.1.gz fakeroot.sv.1.gz %{_mandir}/sv/man1/fakeroot-tcp.1.gz \
  --slave %{_mandir}/sv/man1/faked.1.gz faked.sv.1.gz %{_mandir}/sv/man1/faked-tcp.1.gz

/usr/sbin/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-sysv" 40 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-sysv \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-sysv.so \
  --slave %{_mandir}/man1/fakeroot.1.gz fakeroot.1.gz %{_mandir}/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/man1/faked.1.gz faked.1.gz %{_mandir}/man1/faked-sysv.1.gz \
  --slave %{_mandir}/de/man1/fakeroot.1.gz fakeroot.de.1.gz %{_mandir}/de/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/de/man1/faked.1.gz faked.de.1.gz %{_mandir}/de/man1/faked-sysv.1.gz \
  --slave %{_mandir}/es/man1/fakeroot.1.gz fakeroot.es.1.gz %{_mandir}/es/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/es/man1/faked.1.gz faked.es.1.gz %{_mandir}/es/man1/faked-sysv.1.gz \
  --slave %{_mandir}/fr/man1/fakeroot.1.gz fakeroot.fr.1.gz %{_mandir}/fr/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/fr/man1/faked.1.gz faked.fr.1.gz %{_mandir}/fr/man1/faked-sysv.1.gz \
  --slave %{_mandir}/nl/man1/fakeroot.1.gz fakeroot.nl.1.gz %{_mandir}/nl/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/nl/man1/faked.1.gz faked.nl.1.gz %{_mandir}/nl/man1/faked-sysv.1.gz \
  --slave %{_mandir}/pt/man1/fakeroot.1.gz fakeroot.pt.1.gz %{_mandir}/pt/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/pt/man1/faked.1.gz faked.pt.1.gz %{_mandir}/pt/man1/faked-sysv.1.gz \
  --slave %{_mandir}/sv/man1/fakeroot.1.gz fakeroot.sv.1.gz %{_mandir}/sv/man1/fakeroot-sysv.1.gz \
  --slave %{_mandir}/sv/man1/faked.1.gz faked.sv.1.gz %{_mandir}/sv/man1/faked-sysv.1.gz

%preun
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove fakeroot "%{_bindir}/fakeroot-tcp"
  /usr/sbin/alternatives --remove fakeroot "%{_bindir}/fakeroot-sysv"
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS BUGS DEBUG doc/README.saving
%{_bindir}/faked-*
%ghost %{_bindir}/faked
%{_bindir}/fakeroot-*
%ghost %{_bindir}/fakeroot
%{_mandir}/man1/faked-sysv.1*
%{_mandir}/man1/faked-tcp.1*
%{_mandir}/man1/fakeroot-sysv.1*
%{_mandir}/man1/fakeroot-tcp.1*
%ghost %{_mandir}/man1/faked.1.gz
%ghost %{_mandir}/man1/fakeroot.1.gz
%ghost %lang(de) %{_mandir}/de/man1/faked.1.gz
%ghost %lang(de) %{_mandir}/de/man1/fakeroot.1.gz
%ghost %lang(es) %{_mandir}/es/man1/faked.1.gz
%ghost %lang(es) %{_mandir}/es/man1/fakeroot.1.gz
%ghost %lang(fr) %{_mandir}/fr/man1/faked.1.gz
%ghost %lang(fr) %{_mandir}/fr/man1/fakeroot.1.gz
%ghost %lang(pt) %{_mandir}/pt/man1/faked.1.gz
%ghost %lang(pt) %{_mandir}/pt/man1/fakeroot.1.gz
%ghost %lang(sv) %{_mandir}/sv/man1/faked.1.gz
%ghost %lang(sv) %{_mandir}/sv/man1/fakeroot.1.gz
%ghost %lang(nl) %{_mandir}/nl/man1/faked.1.gz
%ghost %lang(nl) %{_mandir}/nl/man1/fakeroot.1.gz

%files libs
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-sysv.so
%{_libdir}/libfakeroot/libfakeroot-tcp.so
%ghost %{_libdir}/libfakeroot/libfakeroot-0.so

%changelog
* Thu Dec 08 2016 sulit - 1.21-1
- upgrade fakeroot to 1.21
- add automake autoconf libtool buildrequires

* Fri Oct 23 2015 cjacker - 1.20.2-2
- Rebuild for new 4.0 release

* Thu Jun 18 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.20.2-1
- update to 1.20.2
- alternativize libfakeroot and faked as well (bug 817088)
- include Portugese manpages
- add missing BR: libcap-devel
- autogenerate most of the file list

