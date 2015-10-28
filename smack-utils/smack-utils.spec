Name: smack-utils
Version: 1.1.0
Release: 2
Summary: Utilities for configuring Linux SMACK 	

License: GPL	
URL:	 http://schaufler-ca.com/	
Source0: smack-%{version}.tar.gz

BuildRequires: glibc
#for unitdir
BuildRequires: systemd-devel

Requires: systemd

%description
A selection of administration tools for using the smack kernel
interface. This package includes some tools and the init script
for loading and unloading rules and query the policy.

The Simplified Mandatory Access Control Kernel (SMACK) provides a
complete Linux kernel based mechanism for protecting processes and
data from inappropriate manipulation. Smack uses process, file, and
network labels combined with an easy to understand and manipulate
way to identify the kind of accesses that should be allowed.

%package -n libsmack-devel
Summary:        Development files for smack

%description -n libsmack-devel
Library allows applications to work with the smack kernel interface.

The Simplified Mandatory Access Control Kernel (SMACK) provides a
complete Linux kernel based mechanism for protecting processes and
data from inappropriate manipulation. Smack uses process, file, and
network labels combined with an easy to understand and manipulate
way to identify the kind of accesses that should be allowed.

%prep
%setup -q -n smack-%{version}

%build
if [ ! -f "configure" ]; then ./autogen.sh; fi
%configure \
	--disable-shared \
	--enable-static \
	--with-systemdsystemunitdir=%{_unitdir}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

#own folders
mkdir -p %{buildroot}%{_sysconfdir}/smack/accesses.d
mkdir -p %{buildroot}%{_sysconfdir}/smack/cipso.d

pushd %{buildroot}%{_docdir}/libsmack
tar zxf libsmack*.tar.gz
rm -rf libsmack*.tar.gz
popd

%files
%{_sysconfdir}/smack/accesses.d
%{_sysconfdir}/smack/cipso.d
%{_bindir}/chsmack
%{_bindir}/smackaccess
%{_bindir}/smackcipso
%{_bindir}/smackctl
%{_bindir}/smackload
#%{_libdir}/libsmack.so.*
%{_mandir}/man1/smackaccess.1.gz
%{_mandir}/man8/chsmack.8.gz
%{_mandir}/man8/smackcipso.8.gz
%{_mandir}/man8/smackctl.8.gz
%{_mandir}/man8/smackload.8.gz

%files -n libsmack-devel
%{_includedir}/sys/smack.h
#%{_libdir}/libsmack.so
%{_libdir}/libsmack.a
%{_libdir}/pkgconfig/libsmack.pc
%{_docdir}/libsmack/*
%{_mandir}/man3/*

%changelog
* Fri Oct 23 2015 cjacker - 1.1.0-2
- Rebuild for new 4.0 release


