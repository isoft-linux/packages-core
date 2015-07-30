%define majorver 8.6
%define vers %{majorver}.4

Summary: The graphical toolkit for the Tcl scripting language
Name: tk
Version: %{vers}
Release: 2%{?dist}
Epoch:   1
License: TCL
Group: Development/Languages
URL: http://tcl.sourceforge.net
Source0: http://download.sourceforge.net/sourceforge/tcl/%{name}%{version}-src.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcl = %{epoch}:%{version}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: tcl-devel = %{epoch}:%{version}, autoconf
BuildRequires: libX11-devel
BuildRequires: libXft-devel
# panedwindow.n from itcl conflicts
Conflicts: itcl <= 3.2
Obsoletes: tile <= 0.8.2
Provides: tile = 0.8.2
Patch1: tk-8.6.1-make.patch
Patch2: tk-8.6.3-conf.patch
# fix implicit linkage of freetype that breaks xft detection (#677692)
Patch3: tk-8.6.1-fix-xft.patch
Patch4: tk-8.6.4-no-fonts-fix.patch

%description
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

%package devel
Summary: Tk graphical toolkit development files
Group: Development/Languages
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tcl-devel = %{epoch}:%{version}
Requires: libX11-devel libXft-devel

%description devel
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the development files and man pages for tk.

%prep
%setup -n %{name}%{version} -q

%patch1 -p1 -b .make
%patch2 -p1 -b .conf
%patch3 -p1 -b .fix-xft
%patch4 -p1 -b .no-fonts-fix

%build
cd unix
autoconf
%configure --enable-threads
make %{?_smp_mflags} CFLAGS="%{optflags}" TK_LIBRARY=%{_datadir}/%{name}%{majorver}

%check
# do not run "make test" by default since it requires an X display
%{?_with_check: %define _with_check 1}
%{!?_with_check: %define _with_check 0}

%if %{_with_check}
#  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TK_LIBRARY=%{_datadir}/%{name}%{majorver}

ln -s wish%{majorver} %{buildroot}%{_bindir}/wish

# for linking with -l%%{name}
ln -s lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/{generic/ttk,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
  for i in *.h ; do
    [ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
  done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh

%pre
[ ! -h %{_prefix}/%{_lib}/%{name}%{majorver} ] || rm %{_prefix}/%{_lib}/%{name}%{majorver}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/wish*
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tkAppInit.c
%{_libdir}/lib%{name}%{majorver}.so
%{_libdir}/%{name}%{majorver}
%{_mandir}/man1/*
%{_mandir}/mann/*
%doc README changes license.terms

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}stub%{majorver}.a
%{_libdir}/%{name}Config.sh
%{_libdir}/pkgconfig/tk.pc
%{_mandir}/man3/*
%{_datadir}/%{name}%{majorver}/tkAppInit.c

%changelog
