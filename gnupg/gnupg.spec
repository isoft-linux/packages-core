%define libusb0_ver 0.1.5
Summary: A GNU utility for secure communication and data storage
Name: gnupg
Version: 1.4.19
Release: 2 
License: GPLv3+ with exceptions
Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2

URL: http://www.gnupg.org/
BuildRequires: autoconf >= 2.60
BuildRequires: automake, bzip2-devel, ncurses-devel
BuildRequires: readline-devel, zlib-devel, gettext-devel
BuildRequires: libcurl-devel
# pgp-tools, perl-GnuPG-Interface include 'Requires: gpg' -- Rex
Provides: gpg = %{version}-%{release}

%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures. GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC2440. Since GnuPG doesn't use any patented
algorithm, it is not compatible with any version of PGP2 (PGP2.x uses
only IDEA for symmetric-key encryption, which is patented worldwide).

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -fPIE -DPIC" ; export CFLAGS
LDFLAGS="$RPM_OPT_FLAGS -pie -Wl,-z,relro,-z,now" ; export LDFLAGS
export LIBS="-lusb-1.0"

%configure \
    --disable-rpath \
    --disable-ldap \
    --with-zlib \
    --enable-noexecstack \
    $configure_flags \
    --without-libusb \
    --disable-ldap 
make %{?_smp_mflags}

%check
make check

%clean
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m755 lspgpot %{buildroot}%{_bindir}/lspgpot
rm -rf %{buildroot}/%{_infodir}

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_libexecdir}/gnupg
%{_datadir}/%{name}/FAQ
%{_datadir}/%{name}/options.skel
%{_libexecdir}/gnupg/gpgkeys_curl
%{_libexecdir}/gnupg/gpgkeys_finger
%{_libexecdir}/gnupg/gpgkeys_hkp
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_mandir}/man1/gpg-zip.1.gz
%{_mandir}/man1/gpg.1.gz
%{_mandir}/man1/gpgv.1.gz

%changelog
* Fri Oct 23 2015 cjacker - 1.4.19-2
- Rebuild for new 4.0 release

