Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.21
Release: 1 
License: GPL
URL: http://www.gnu.org/software/grep/

Source0: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz

Source1: colorgrep.sh
Source3: GREP_COLORS
Source4: grepconf.sh

# upstream ticket 39444
Patch0: grep-2.21-man-fix-gs.patch
# upstream ticket 39445
Patch1: grep-2.21-help-align.patch
# fix buffer overrun for grep -F, rhbz#1183653
Patch2: grep-2.21-buf-overrun-fix.patch
# backported from upstream
# http://git.savannah.gnu.org/cgit/grep.git/commit/?id=c8b9364d5900a40809827aee6cc53705073278f6
Patch3: grep-2.21-recurse-behaviour-change-doc.patch
# http://www.mail-archive.com/bug-gnulib%40gnu.org/msg31638.html
Patch4: grep-2.21-gnulib.patch

Buildrequires: pcre-devel >= 3.9-10, gettext, gzip

%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%prep
%setup -q
%patch0 -p1 -b .man-fix-gs
%patch1 -p1 -b .help-align
%patch2 -p1 -b .buf-overrun-fix
%patch3 -p1 -b .recurse-behaviour-change-doc
%patch4 -p1 -b .gnulib

chmod 755 tests/kwset-abuse

%build
[ ! -e configure ] && ./autogen.sh
%global BUILD_FLAGS $RPM_OPT_FLAGS

# Currently gcc on ppc uses double-double arithmetic for long double and it
# does not conform to the IEEE floating-point standard. Thus force
# long double to be double and conformant.
%ifarch ppc ppc64
%global BUILD_FLAGS %{BUILD_FLAGS} -mlong-double-64
%endif

%configure --without-included-regex --disable-silent-rules \
  CPPFLAGS="-I%{_includedir}/pcre" CFLAGS="%{BUILD_FLAGS}"

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall LDFLAGS=-s prefix=${RPM_BUILD_ROOT}%{_prefix} exec_prefix=${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install -Dpm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_libexecdir}/grepconf.sh

rm -rf $RPM_BUILD_ROOT%{_infodir}

%find_lang grep

%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f grep.lang 
%defattr(-,root,root)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/profile.d/colorgrep.*sh
%config(noreplace) %{_sysconfdir}/GREP_COLORS
%{_libexecdir}/grepconf.sh
%{_mandir}/*/*

%changelog
* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
