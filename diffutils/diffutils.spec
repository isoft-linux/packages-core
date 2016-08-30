Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 3.5
Release: 1
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz
License: GPL

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

%prep
%setup -q

%build
%configure
make PR_PROGRAM=%{_bindir}/pr

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -rf $RPM_BUILD_ROOT%{_infodir}

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Tue Aug 30 2016 sulit <sulitsrc@gmail.com> - 3.5-1
- update diffutils to 3.5

* Fri Oct 23 2015 cjacker - 3.3-2
- Rebuild for new 4.0 release

