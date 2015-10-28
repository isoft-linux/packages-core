%define majorver 8.6
%define	vers %{majorver}.4
%define sdt 0 

Summary: Tool Command Language, pronounced tickle
Name: tcl
Version: %{vers}
Release: 2%{?dist}
Epoch: 1
License: TCL
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
Buildrequires: autoconf
BuildRequires: zlib-devel
Provides: tcl(abi) = %{majorver}
Obsoletes: tcl-tcldict <= %{vers}
Provides: tcl-tcldict = %{vers}
Patch0: tcl-8.6.3-autopath.patch
Patch1: tcl-8.6.3-conf.patch
Patch2: tcl-8.6.3-hidden.patch

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package devel
Summary: Tcl scripting language development environment
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

%prep
%setup -q -n %{name}%{version}
rm -r compat/zlib
chmod -x generic/tclStrToD.c

%patch0 -p1 -b .autopath
%patch1 -p1 -b .conf
%patch2 -p1 -b .hidden

%build
pushd unix
autoconf
%configure \
%if %sdt
--enable-dtrace \
%endif
--enable-threads \
--enable-symbols \
--enable-shared

make %{?_smp_mflags} CFLAGS="%{optflags}" TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

%check
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%if ! %{_without_check}
  cd unix
  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

ln -s tclsh%{majorver} %{buildroot}%{_bindir}/tclsh

# for linking with -lib%%{name}
ln -s lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}/%{_libdir}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/%{name}Config.sh %{buildroot}/%{_libdir}/%{name}%{majorver}/%{name}Config.sh

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/{generic,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
	done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh
rm -rf %{buildroot}/%{_datadir}/%{name}%{majorver}/ldAix

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/tclsh*
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tclAppInit.c
%{_datadir}/%{name}8
%{_libdir}/lib%{name}%{majorver}.so
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/mann/*
%dir %{_libdir}/%{name}%{majorver}
%doc README changes 
%doc license.terms

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/lib%{name}stub%{majorver}.a
%{_libdir}/lib%{name}.so
%{_libdir}/%{name}Config.sh
%{_libdir}/%{name}ooConfig.sh
%{_libdir}/%{name}%{majorver}/%{name}Config.sh
%{_libdir}/pkgconfig/tcl.pc
%{_datadir}/%{name}%{majorver}/tclAppInit.c

%changelog
* Fri Oct 23 2015 cjacker - 1:8.6.4-2
- Rebuild for new 4.0 release

