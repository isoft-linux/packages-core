Summary: Programs for accessing MS-DOS disks without mounting the disks.
Name: mtools
Version: 4.0.18
Release: 2.2.1
License: GPL
Source: http://mtools.linux.lu/mtools-%{version}.tar.gz
Patch0: mtools-fix-build-with-clang.patch
Url: http://mtools.linux.lu/


%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 XDF disks, and 2m disks.

Mtools should be installed if you need to use MS-DOS disks.

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc $RPM_BUILD_ROOT/%{_infodir}

%makeinstall

install -m644 mtools.conf $RPM_BUILD_ROOT/etc
rm -rf $RPM_BUILD_ROOT/%{_infodir}/*

# We aren't shipping this.
find $RPM_BUILD_ROOT -name "floppyd*" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config /etc/mtools.conf
/usr/bin/*
%{_mandir}/*/*

%changelog
* Fri Oct 23 2015 cjacker - 4.0.18-2.2.1
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

