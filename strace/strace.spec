Summary: Tracks and displays system calls associated with a running process
Name: strace
Version: 4.10
Release: 2
License: BSD
URL: http://sourceforge.net/projects/strace/
Source0: http://dl.sourceforge.net/strace/%{name}-%{version}.tar.xz
BuildRequires: libacl-devel

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%prep
%setup -q
%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_bindir}/strace-graph

%check
make check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*


%changelog
* Fri Oct 23 2015 cjacker - 4.10-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

