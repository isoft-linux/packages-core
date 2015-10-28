%global prerel pre6

Name:      elinks
Summary:   A text-mode Web browser
Version:   0.12
Release:   0.48.%{prerel}%{?dist}
License:   GPLv2
URL:       http://elinks.or.cz
Source:    http://elinks.or.cz/download/elinks-%{version}%{prerel}.tar.bz2
Source2:   elinks.conf

BuildRequires: automake
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: gpm-devel
BuildRequires: js-devel
BuildRequires: krb5-devel
#BuildRequires: libidn2-devel
BuildRequires: lua-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel
Requires(preun): %{_sbindir}/alternatives
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(postun): coreutils
Requires(postun): %{_sbindir}/alternatives
Provides:  webclient
Provides:  links = 1:0.97-1
Provides: text-www-browser

Patch0: elinks-0.11.0-ssl-noegd.patch
Patch1: elinks-0.10.1-utf_8_io-default.patch
Patch3: elinks-0.11.0-getaddrinfo.patch
Patch4: elinks-0.11.0-sysname.patch
Patch5: elinks-0.10.1-xterm.patch
Patch7: elinks-0.11.3-macropen.patch
Patch8: elinks-scroll.patch
Patch11: elinks-0.12pre5-js185.patch
Patch12: elinks-0.12pre5-ddg-search.patch
Patch13: elinks-0.12pre6-autoconf.patch
Patch14: elinks-0.12pre6-ssl-hostname.patch
Patch15: elinks-0.12pre6-list_is_singleton.patch
Patch16: elinks-0.12pre6-lua51.patch
Patch17: elinks-0.12pre6-libidn2.patch

%description
Elinks is a text-based Web browser. Elinks does not display any images,
but it does support frames, tables and most other HTML tags. Elinks'
advantage over graphical browsers is its speed--Elinks starts and exits
quickly and swiftly displays Web pages.

%prep
%setup -q -n %{name}-%{version}%{prerel}

# Prevent crash when HOME is unset (bug #90663).
%patch0 -p1

# UTF-8 by default
%patch1 -p1

# Make getaddrinfo call use AI_ADDRCONFIG.
%patch3 -p1

# Don't put so much information in the user-agent header string (bug #97273).
%patch4 -p1

# Fix xterm terminal: "Linux" driver seems better than "VT100" (#128105)
%patch5 -p1

# fix for open macro in new glibc
%patch7 -p1

#upstream fix for out of screen dialogs
%patch8 -p1

# backported upstream commits f31cf6f, 2844f8b, 218a225, and 12803e4
%patch11 -p1

# add default "ddg" dumb/smart rewrite prefixes for DuckDuckGo (#856348)
%patch12 -p1

# add missing AC_LANG_PROGRAM around the first argument of AC_COMPILE_IFELSE
%patch13 -p1

# verify server certificate hostname with OpenSSL (#881411)
%patch14 -p1

# let list_is_singleton() return false for an empty list (#1075415)
%patch15 -p1

# use later versions of lua since lua50 is not available (#1098392)
%patch16 -p1

# add support for GNU Libidn2, patch by Robert Scheck (#1098789)
%patch17 -p1

# rename the input file of autoconf to eliminate a warning
mv -v configure.in configure.ac
sed -e 's/configure\.in/configure.ac/' \
    -i Makefile* acinclude.m4 doc/man/man1/Makefile

# remove bogus serial numbers
sed -i 's/^# *serial [AM0-9]*$//' acinclude.m4 config/m4/*.m4

# we need to recreate autotools files because of the NSS patch
aclocal -I config/m4
autoconf
autoheader

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -D_GNU_SOURCE"
%configure %{?rescue:--without-gpm} \
    --enable-256-colors             \
    --enable-bittorrent             \
    --with-gssapi                   \
    --with-lua                      \
    --with-openssl                  \
    --without-gnutls                \
    --without-x

# uncomment to turn off optimizations
#sed -i 's/-O2/-O0/' Makefile.config

MOPTS="V=1"
if tty >/dev/null 2>&1; then
    # turn on fancy colorized output only when we have a TTY device
    MOPTS=
fi
make %{?_smp_mflags} $MOPTS

%install
make install DESTDIR=$RPM_BUILD_ROOT V=1
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/elinks.conf
touch $RPM_BUILD_ROOT%{_bindir}/links
true | gzip -c > $RPM_BUILD_ROOT%{_mandir}/man1/links.1.gz
%find_lang elinks

%postun
if [ "$1" -ge "1" ]; then
	links=`readlink %{_sysconfdir}/alternatives/links`
	if [ "$links" == "%{_bindir}/elinks" ]; then
		%{_sbindir}/alternatives --set links %{_bindir}/elinks
	fi
fi
exit 0

%post
#Set up alternatives files for links
%{_sbindir}/alternatives --install %{_bindir}/links links %{_bindir}/elinks 90 \
  --slave %{_mandir}/man1/links.1.gz links-man %{_mandir}/man1/elinks.1.gz
links=`readlink %{_sysconfdir}/alternatives/links`
if [ "$links" == "%{_bindir}/elinks" ]; then
	%{_sbindir}/alternatives --set links %{_bindir}/elinks
fi


%preun
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove links %{_bindir}/elinks
fi
exit 0

%files -f elinks.lang
%doc README SITES TODO COPYING
%ghost %verify(not md5 size mtime) %{_bindir}/links
%{_bindir}/elinks
%ghost %verify(not md5 size mtime) %{_mandir}/man1/links.1.gz
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%changelog
* Fri Oct 23 2015 cjacker - 0.12-0.48.pre6
- Rebuild for new 4.0 release

