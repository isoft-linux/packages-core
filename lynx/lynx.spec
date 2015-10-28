Summary: A text-based Web browser
Name: lynx
Version: 2.8.7
Release: 8
License: GPLv2
Source: http://lynx.isc.org/lynx%{version}/lynx%{version}.tar.bz2
URL: http://lynx.isc.org/
Patch0: lynx-2.8.6-default-config.patch
Patch1: lynx-2.8.6-backgrcolor.patch
Patch2: lynx-build-fixes.patch
Patch3: lynx-CVE-2008-4690.patch
Patch4: lynx-2.8.7-bm-del.patch
Patch5: lynx-2.8.7-locale.patch
Patch6: lynx-2.8.7-ipv6arg.patch
Patch7: lynx-2.8.7-alloca.patch
Patch8: lynx-2.8.7-bz679266.patch

Provides: webclient
Provides: text-www-browser
BuildRequires: gettext
BuildRequires: openssl-devel
BuildRequires: ncurses-devel
BuildRequires: slang-devel
BuildRequires: unzip
BuildRequires: zip
BuildRequires: zlib-devel
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Lynx is a text-based Web browser. Lynx does not display any images,
but it does support frames, tables, and most other HTML tags. One
advantage Lynx has over graphical browsers is speed; Lynx starts and
exits quickly and swiftly displays web pages.

%prep
%setup -q -n lynx2-8-7

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

perl -pi -e "s,^HELPFILE:.*,HELPFILE:file://localhost/usr/share/doc/lynx-%{version}/lynx_help/lynx_help_main.html,g" lynx.cfg
perl -pi -e "s,^DEFAULT_INDEX_FILE:.*,DEFAULT_INDEX_FILE:http://www.google.com/,g" lynx.cfg
perl -pi -e 's,^#LOCALE_CHARSET:.*,LOCALE_CHARSET:TRUE,' lynx.cfg

%build
CFLAGS="-ggdb $RPM_OPT_FLAGS -DNCURSES -DNCURSES_MOUSE_VERSION" ; export CFLAGS
CXXFLAGS="-ggdb $RPM_OPT_FLAGS -DNCURSES -DNCURSES_MOUSE_VERSION" ; export CXXFLAGS
if pkg-config openssl ; then
    CPPFLAGS=`pkg-config --cflags openssl` ; export CPPFLAGS
    LDFLAGS=`pkg-config --libs-only-L openssl` ; export LDFLAGS
fi
%configure --libdir=/etc            \
    --disable-font-switch           \
    --enable-addrlist-page          \
    --enable-charset-choice         \
    --enable-cgi-links              \
    --enable-cjk                    \
    --enable-default-colors         \
    --enable-externs                \
    --enable-file-upload            \
    --enable-internal-links         \
    --enable-ipv6                   \
    --enable-japanese-utf8          \
    --enable-justify-elts           \
    --enable-locale-charset         \
    --enable-kbd-layout             \
    --enable-libjs                  \
    --enable-nls                    \
    --enable-nsl-fork               \
    --enable-persistent-cookies     \
    --enable-prettysrc              \
    --enable-read-eta               \
    --enable-scrollbar              \
    --enable-source-cache           \
    --enable-warnings               \
    --with-screen=ncursesw          \
    --with-ssl=%{_libdir}           \
    --with-zlib

# uncomment to turn off optimizations
#find -name makefile | xargs sed -i 's/-O2/-O0/'

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
chmod -x samples/mailto-form.pl
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1 libdir=$RPM_BUILD_ROOT/etc

cat >$RPM_BUILD_ROOT%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/lynx
%{_mandir}/*/*
%config %{_sysconfdir}/lynx.cfg
%config(noreplace) %{_sysconfdir}/lynx.lss
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg

%changelog
* Fri Oct 23 2015 cjacker - 2.8.7-8
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

