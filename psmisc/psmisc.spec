
Summary: Utilities for managing processes on your system
Name: psmisc
Version: 22.21
Release: 7
License: GPLv2+
Group: Applications/System
URL: http://sourceforge.net/projects/psmisc

Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires: gettext
BuildRequires: ncurses-devel
BuildRequires: autoconf automake


%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.

%prep
%setup -q


%build
%configure --prefix=%{_prefix} 
make %{?_smp_mflags}


%install
make install DESTDIR="$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/fuser $RPM_BUILD_ROOT%{_sbindir}

%find_lang %name


%files -f %{name}.lang
%{_sbindir}/fuser
%{_bindir}/killall
%{_bindir}/pstree
%{_bindir}/pstree.x11
%{_bindir}/prtstat
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*
%{_mandir}/man1/prtstat.1*
%{_bindir}/peekfd
%{_mandir}/man1/peekfd.1*


%changelog
