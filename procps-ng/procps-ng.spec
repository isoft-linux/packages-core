Name:		procps-ng
Version:    3.3.10	
Release:	1
Summary:	Utilities for monitoring your system and its processes

Group:	    Core/Runtime/Utility 
License:	GPL
URL:		http://sourceforge.net/projects/procps-ng
Source0:	%{name}-%{version}.tar.xz
Patch0:     procps-ng-use-correct-scanf-format.patch
Provides:   procps
BuildRequires: expect
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Core/Development/Library
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure \
    --prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/sbin \
    exec_prefix=/ \
    --with-systemd 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
#provides in util-linux
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/kill.*
rm -rf $RPM_BUILD_ROOT%{_bindir}/kill

#do not ship too many readmes 
rm -rf $RPM_BUILD_ROOT%{_docdir}

%find_lang procps-ng

rpmclean

%check
#some case failed.
make check ||:

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ -x /usr/bin/busybox ]; then
    /usr/bin/busybox --install -s
fi


%files -f procps-ng.lang
%{_bindir}/ps
%{_bindir}/free
%{_bindir}/pgrep
%{_bindir}/pidof
%{_bindir}/pkill
%{_bindir}/pmap
%{_bindir}/pwdx
%{_bindir}/slabtop
%{_bindir}/tload
%{_bindir}/top
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/w
%{_bindir}/watch
%{_sbindir}/sysctl

%{_libdir}/libprocps.so.*
%{_mandir}/man1/free.1.gz
%{_mandir}/man1/pgrep.1.gz
%{_mandir}/man1/pidof.1.gz
%{_mandir}/man1/pkill.1.gz
%{_mandir}/man1/pmap.1.gz
%{_mandir}/man1/ps.1.gz
%{_mandir}/man1/pwdx.1.gz
%{_mandir}/man1/slabtop.1.gz
%{_mandir}/man1/tload.1.gz
%{_mandir}/man1/top.1.gz
%{_mandir}/man1/uptime.1.gz
%{_mandir}/man1/w.1.gz
%{_mandir}/man1/watch.1.gz
%{_mandir}/man5/sysctl.conf.5.gz
%{_mandir}/man8/sysctl.8.gz
%{_mandir}/man8/vmstat.8.gz

%files devel
%{_includedir}/proc
%{_libdir}/libprocps.a
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
%{_mandir}/man3/openproc.3.gz
%{_mandir}/man3/readproc.3.gz
%{_mandir}/man3/readproctab.3.gz
