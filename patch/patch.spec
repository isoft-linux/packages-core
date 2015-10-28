Summary: The GNU patch command, for modifying/upgrading files.
Name: patch
Version: 2.7.5
Release: 2 
License: GPL
URL: http://www.gnu.org/software/patch/patch.html
Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.xz

#for make check with busybox cat
Patch0: patch-test-fix-cat-without-ve-option.patch
#disable ed related checks, it works, but we do not want to depend on ed here.
Patch1: patch-disable-ed-related-test.patch

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/*
%{_mandir}/*/*

%changelog
* Fri Oct 23 2015 cjacker - 2.7.5-2
- Rebuild for new 4.0 release

