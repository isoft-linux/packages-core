Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.27
Release: 1
License: GPL
URL: http://www.gnu.org/software/grep/

Source0: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz

Source1: colorgrep.sh
Source2: colorgrep.csh
Source3: GREP_COLORS
Source4: grepconf.sh

# upstream ticket 39444
Patch0: grep-2.22-man-fix-gs.patch
# upstream ticket 39445
Patch1: grep-2.22-help-align.patch

Buildrequires: pcre-devel >= 3.9-10, gettext, gzip
BuildRequires: autoconf automake

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
install -pm 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
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
* Thu Dec 15 2016 sulit - 2.27-1
- upgrade grep to 2.27

* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 2.25-1
- update grep to 2.25

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 2.22-2
- Update

* Fri Oct 23 2015 cjacker - 2.21-2
- Rebuild for new 4.0 release

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
