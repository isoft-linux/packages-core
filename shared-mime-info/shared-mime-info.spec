Summary: Shared MIME information database
Name: shared-mime-info
Version: 1.4
Release: 4
License: GPLv2+
Group:  Framework/Runtime/Utility 
URL: http://freedesktop.org/Software/shared-mime-info
Source0: http://people.freedesktop.org/~hadess/%{name}-%{version}.tar.xz
Source1: defaults.list
# Generated with:
# for i in `cat /home/hadess/Projects/jhbuild/totem/data/mime-type-list.txt | grep -v real | grep -v ^#` ; do if grep MimeType /home/hadess/Projects/jhbuild/rhythmbox/data/rhythmbox.desktop.in.in | grep -q "$i;" ; then echo "$i=rhythmbox.desktop;totem.desktop;" >> totem-defaults.list ; else echo "$i=totem.desktop;" >> totem-defaults.list ; fi ; done ; for i in `cat /home/hadess/Projects/jhbuild/totem/data/uri-schemes-list.txt | grep -v ^#` ; do echo "x-scheme-handler/$i=totem.desktop;" >> totem-defaults.list ; done
Source2: totem-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/gnome-file-roller.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do if ! `grep -q $i defaults.list` ; then echo $i=gnome-file-roller.desktop\; >> file-roller-defaults.list ; fi ; done
Source3: file-roller-defaults.list
# Generated with:
# for i in `grep MimeType= /usr/share/applications/shotwell-viewer.desktop | sed 's/MimeType=//' | sed 's/;/ /g'` ; do echo $i=shotwell-viewer.desktop\; >> shotwell-viewer-defaults.list ; done
Source4: shotwell-viewer-defaults.list

# Work-around for https://bugs.freedesktop.org/show_bug.cgi?id=40354
Patch0: 0001-Remove-sub-classing-from-OO.o-mime-types.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
BuildRequires:  gettext
# For intltool:
BuildRequires: perl(XML::Parser) intltool
Requires: pkgconfig

Requires(post): glib2

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%prep
%setup -q
%patch0 -p1 -b .ooo-zip

%build

%configure --disable-update-mimedb
# make %{?_smp_mflags}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/%{_datadir}/applications/defaults.list
cat %SOURCE2 >> $RPM_BUILD_ROOT/%{_datadir}/applications/defaults.list
cat %SOURCE3 >> $RPM_BUILD_ROOT/%{_datadir}/applications/defaults.list
cat %SOURCE4 >> $RPM_BUILD_ROOT/%{_datadir}/applications/defaults.list

## remove bogus translation files
## translations are already in the xml file installed
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/*

%post
# Should fail, as it would mean a problem in the mime database
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README NEWS HACKING COPYING shared-mime-info-spec.xml
%{_bindir}/*
%dir %{_datadir}/mime/
%{_datadir}/mime/packages
%{_datadir}/applications/defaults.list
%{_datadir}/pkgconfig/*
%{_mandir}/man*/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

