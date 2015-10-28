Name:           kbd
Version:        2.0.2 
Release:        11 
Summary:        Tools for configuring the console (keyboard, virtual terminals, etc.)

License:        GPLv2+
URL:            http://ftp.altlinux.org/pub/people/legion/kbd
Source0:        http://ftp.altlinux.org/pub/people/legion/kbd/kbd-%{version}.tar.xz
Source10:       error.h

Patch10:        0001-Replace-u_short-with-unsigned-short.patch
Patch11:        0002-Fix-required-header-includes.patch
Patch12:        0003-Only-inluclude-kernel-headers-with-glibc.patch
Patch13:        kbd-2.0.2-backspace-1.patch

BuildRequires:  bison, flex, gettext, check-devel
Conflicts:      util-linux < 2.11r-9
Requires:       systemd 
ExcludeArch:    s390 s390x
Obsoletes: open
%description
The %{name} package contains tools for managing a Linux
system's console's behavior, including the keyboard, the screen
fonts, the virtual terminals and font files.

%prep
%setup -q
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

cp %{SOURCE10} .
    # fixes from fedora
    # 7-bit maps are obsolete; so are non-euro maps
pushd data/keymaps/i386
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv dvorak/no.map dvorak/no-dvorak.map
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
popd

%build
%configure --prefix=%{_prefix} --datadir=/lib/kbd --mandir=%{_mandir} --localedir=%{_datadir}/locale
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# ro_win.map.gz is useless
rm -f $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/ko.map.gz

# Move binaries which we use before /usr is mounted from %{_bindir} to /bin.
mkdir -p $RPM_BUILD_ROOT/bin
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop loadkeys ; do
  mv $RPM_BUILD_ROOT%{_bindir}/$binary $RPM_BUILD_ROOT/bin/
done

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,/bin/kbd_mode,g;s,\<setfont\>,/bin/setfont,g' \
        $RPM_BUILD_ROOT/bin/unicode_start

# Link open to openvt
ln -s openvt $RPM_BUILD_ROOT%{_bindir}/open

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
/lib/kbd

%changelog
* Fri Oct 23 2015 cjacker - 2.0.2-11
- Rebuild for new 4.0 release

