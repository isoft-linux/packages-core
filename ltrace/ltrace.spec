Summary: Tracks runtime library calls from dynamically linked executables
Name: ltrace
Version: 0.7.3
Release: 1 
License: GPLv2+
Group: CoreDev/Development/Utility
URL: http://ltrace.alioth.debian.org/
#git clone git://git.debian.org/git/collab-maint/ltrace.git
Source: ltrace.tar.gz
BuildRequires: libelfutils-devel
ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64 s390 s390x alpha sparc


%description
Ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process.  Ltrace can also
intercept and print system calls executed by the process.

You should install ltrace if you need a sysadmin tool for tracking the
execution of processes.

%prep
%setup -q -n ltrace

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi

%configure \
    --without-libunwind \
    --disable-werror
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} docdir=%{_docdir}/ltrace-%{version}/ install

%check
echo ====================TESTING=========================
make check ||: 
echo ====================TESTING END=====================

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/ltrace
%{_mandir}/man1/ltrace.1*
%{_mandir}/man5/ltrace.conf.*
%dir %{_datadir}/ltrace
%{_datadir}/ltrace/*
%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

