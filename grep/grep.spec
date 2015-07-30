Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.21
Release: 1 
License: GPL
Group:  Core/Runtime/Utility
Source: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz
URL: http://www.gnu.org/software/grep/
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

%build
[ ! -e configure ] && ./autogen.sh
%configure
make CFLAGS="$RPM_OPT_FLAGS -I%{_includedir}/pcre" MAKEINFO=true


%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall LDFLAGS=-s prefix=${RPM_BUILD_ROOT}%{_prefix} exec_prefix=${RPM_BUILD_ROOT} MAKEINFO=true
rm -rf $RPM_BUILD_ROOT%{_infodir}

%find_lang grep
rpmclean

%check
make check MAKEINFO=true

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f grep.lang 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
