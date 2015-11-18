%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define generate_rpmpriorities 0
%define comps %{_datadir}/comps/%{_build_arch}/comps.xml

%define aptver 0.5.15lorg3.95
%define snapver git522
%define srcver %{aptver}.%{snapver}

Summary: Debian's Advanced Packaging Tool with RPM support
Name: apt
Version: %{aptver}
Release: 27.%{snapver}
URL: http://apt-rpm.org/
# SourceLicense: GPLv2+ except lua/ which is MIT
License: GPLv2+ 

Source0: http://apt-rpm.org/testing/%{name}-%{srcver}.tar.bz2

# user editable template configs
Source1: apt.conf
Source2: sources.list
Source3: vendors.list
Source4: apt_preferences

# rpmpriorities generated + manually tweaked from comps.xml core group
Source5: rpmpriorities
Source19: comps2prio.xsl

# Sources 50-99 are for Lua-scripts not in contrib/
Source51: upgradevirt.lua
Source52: gpg-check.lua

# 150-199 for apt.conf.d
# "factory defaults"
Source150: default.conf

# Fix ppc mapping
Patch0: apt-0.5.15lorg3.2-ppc.patch
# band aid for mmap issues (#211254)
Patch1: apt-0.5.15lorg3.x-cache-corruption.patch
# fix build with gcc 4.7
Patch2: apt-0.5.15lorg3.95-gcc47.patch
# fix build with lua 5.2
Patch3: apt-0.5.15lorg3.95-lua-5.2d.patch
# fix format-security issue
Patch4: apt-0.5.15lorg3.95-format-security.patch
# Fix to build against modern rpm
Patch5: apt-0.5.15lorg3.95-rpm-suggest-fix.patch
# Fix for lua 5.3
Patch6: apt-0.5.15lorg3.95-lua-5.3.patch

#isoftapp patches, only applied to static build.
#use own config files and data dir.
# merged into Patch11 by fujiang.
#Patch10: apt-isoftapp-use-own-conf-method-data-dir.patch
# iSOFT App skeleton implemented by fujiang and Leslie Zhai
Patch11: 0001-isoft-app-skeleton.patch

# TODO: verify the required minimum Python version
BuildRequires: autoconf automake m4 libtool
BuildRequires: python-devel >= 2.2
BuildRequires: swig
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: librpm-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: libstdc++-devel
BuildRequires: gettext
BuildRequires: perl
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gawk
%if %{generate_rpmpriorities}
BuildRequires: %{_bindir}/xsltproc
BuildRequires: %{comps}
%endif
# libxml2-devel, #183689
BuildRequires: pkgconfig
BuildRequires: lua-devel >= 5.3
Requires: gnupg
Requires: bzip2
Requires: os-release
%if 0%{?_without_list:1}
Obsoletes: %{name}-plugins-list < %{version}-%{release}
%endif
%if 0%{?_without_log:1}
Obsoletes: %{name}-plugins-log < %{version}-%{release}
%endif

%description
APT-RPM is a port of Debian's apt tools for RPM based distributions.
It provides the apt-get utility that provides a simple, safe way to
install and upgrade packages. APT features complete installation
ordering, multiple source capability and several other useful
features.

%package -n isoftapp 
Summary: Modified APT-RPM to support iSoft AppDB

%description -n isoftapp
Modified APT-RPM to support iSoft AppDB

%package devel
Summary: Development files and documentation for APT's libapt-pkg
Requires: %{name} = %{version}-%{release}
Requires: librpm-devel
Requires: pkgconfig

%description devel
This package contains development files for developing with APT's
libapt-pkg package manipulation library, modified for RPM.

%package plugins-list
Summary: Additional commands to list extra packages and leaves
Requires: %{name} = %{version}-%{release}

%description plugins-list
This package adds commands for listing all installed packages which
are not availabe in any online repository, and packages that are not
required by any other installed package:
apt-cache list-extras
apt-cache list-nodeps

%package plugins-log
Summary: Log the changes being introduced by the transaction
Requires: %{name} = %{version}-%{release}

%description plugins-log
This script will log the changes being introduced by
the transaction which is going to be run, and is based
on an idea of Panu Matilainen.

When some transaction is run, it will dump information
about it in /var/log/apt.log, or in the configured file.


%prep
%setup -q -c

#apply common patches.
pushd %{name}-%{srcver}
%patch0 -p1 -b .ppc
%patch1 -p0 -b .mmap
%patch2 -p1 -b .gcc47
%patch3 -p1 -b .lua-52
%patch4 -p1 -b .format-security
%patch5 -p1 -b .rpm-suggest-fix
%patch6 -p1 -b .lua-53

install -pm 644 %{SOURCE19} comps2prio.xsl
# don't require python, lua etc because of stuff in doc/contrib
find contrib/ -type f | xargs chmod 0644

popd

#cp original apt to apt-<version>-isoftapp, and apply our isoftapp customized pactch
cp -r %{name}-%{srcver} %{name}-%{srcver}-isoftapp
pushd %{name}-%{srcver}-isoftapp
%patch11 -p1 -b .isoftapp
popd


%build
#build common apt.
pushd %{name}-%{srcver}

CXXFLAGS="%{optflags} -DLUA_COMPAT_MODULE"
%configure --disable-static

make %{?_smp_mflags}

cp -p %{SOURCE5} rpmpriorities
%if %{generate_rpmpriorities}
xsltproc -o rpmpriorities comps2prio.xsl %{comps}
%endif
popd #common apt.

#static build apt with isoftapp support
pushd %{name}-%{srcver}-isoftapp
autoreconf -ivf
CXXFLAGS="%{optflags} -DLUA_COMPAT_MODULE"
%configure --enable-static --disable-shared
make %{?_smp_mflags}

cp -p %{SOURCE5} rpmpriorities
%if %{generate_rpmpriorities}
xsltproc -o rpmpriorities comps2prio.xsl %{comps}
%endif

popd #apt with isoftapp support.

%install
#install common apt.
pushd %{name}-%{srcver}
make install DESTDIR=%{buildroot} includedir=%{_includedir}/apt-pkg

# The state files
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/genpkglist
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/gensrclist
mkdir -p %{buildroot}%{_localstatedir}/lib/apt/lists/partial

# The config files
mkdir -p %{buildroot}%{_sysconfdir}/apt
mkdir -p %{buildroot}%{_sysconfdir}/apt/apt.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/apt/sources.list.d
mkdir -p %{buildroot}%{_sysconfdir}/apt/vendors.list.d
install -pm 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/apt/apt.conf
install -pm 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/apt/sources.list
install -pm 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/apt/vendors.list
install -pm 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/apt/preferences
install -pm 644 rpmpriorities %{buildroot}/%{_sysconfdir}/apt/

# install config parts
install -pm 644 %{SOURCE150} %{buildroot}%{_sysconfdir}/apt/apt.conf.d/

# Lua scripts
mkdir -p %{buildroot}%{_datadir}/apt/scripts
for script in %{SOURCE51} %{SOURCE52} ; do
 install -pm 755 $script %{buildroot}%{_datadir}/apt/scripts
done

# apt-plugins-list from contrib
%if 0%{!?_without_list:1}
install -pm 755 contrib/list-extras/list-extras.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/list-extras/list-extras.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
install -pm 755 contrib/list-nodeps/list-nodeps.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/list-nodeps/list-nodeps.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
%endif

# apt-plugins-log from contrib
%if 0%{!?_without_log:1}
install -pm 755 contrib/log/log.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/log/log.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
%endif

# nuke .la files
rm -f %{buildroot}%{_libdir}/*.la

popd #end installation of common apt.



#install static build apt-get with isoftapp support.
#what we need is 'apt-get', also we rename it to 'app-get'
pushd %{name}-%{srcver}-isoftapp
install -m 0755 cmdline/apt-get %{buildroot}/%{_bindir}/isoftapp

#install own method copy.
pushd methods
make install DESTDIR=%{buildroot}
popd

# The state files
mkdir -p %{buildroot}%{_localstatedir}/cache/isoftapp/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/cache/isoftapp/genpkglist
mkdir -p %{buildroot}%{_localstatedir}/cache/isoftapp/gensrclist
mkdir -p %{buildroot}%{_localstatedir}/lib/isoftapp/lists/partial

# The config files
mkdir -p %{buildroot}%{_sysconfdir}/isoftapp
mkdir -p %{buildroot}%{_sysconfdir}/isoftapp/isoftapp.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/isoftapp/sources.list.d
mkdir -p %{buildroot}%{_sysconfdir}/isoftapp/vendors.list.d
install -pm 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/isoftapp/isoftapp.conf
install -pm 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/isoftapp/sources.list
install -pm 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/isoftapp/vendors.list
install -pm 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/isoftapp/preferences
install -pm 644 rpmpriorities %{buildroot}/%{_sysconfdir}/isoftapp/

# install config parts
install -pm 644 %{SOURCE150} %{buildroot}%{_sysconfdir}/isoftapp/isoftapp.conf.d/

# Lua scripts
mkdir -p %{buildroot}%{_datadir}/isoftapp/scripts

popd #end of isoftapp

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
#the build dir layout changed. we comment out this now.
#doc AUTHORS* COPYING* ABOUT* TODO comps2prio.xsl doc/examples/ contrib/
#doc ChangeLog

%dir %{_sysconfdir}/apt/
%config(noreplace) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %{_sysconfdir}/apt/preferences
%config(noreplace) %{_sysconfdir}/apt/rpmpriorities
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%dir %{_sysconfdir}/apt/apt.conf.d/
# NOTE: no noreplace because we WANT to be able to change the defaults
# without user intervention!
%config %{_sysconfdir}/apt/apt.conf.d/default.conf
%config %{_sysconfdir}/apt/apt.conf.d/multilib.conf
%dir %{_sysconfdir}/apt/sources.list.d/
%dir %{_sysconfdir}/apt/vendors.list.d/

%{_bindir}/apt-cache
%{_bindir}/apt-cdrom
%{_bindir}/apt-config
%{_bindir}/apt-shell
%{_bindir}/apt-get
%{_bindir}/countpkglist
%{_bindir}/genpkglist
%{_bindir}/gensrclist
%{_bindir}/genbasedir
%{_libdir}/libapt-pkg*.so.*
%{_libdir}/apt/
%dir %{_datadir}/apt/
%dir %{_datadir}/apt/scripts/
%{_datadir}/apt/scripts/gpg-check.lua
%{_datadir}/apt/scripts/upgradevirt.lua
%{_localstatedir}/cache/apt/
%{_localstatedir}/lib/apt/
%{_mandir}/man[58]/*.[58]*

%files -n isoftapp
%dir %{_sysconfdir}/isoftapp/
%config(noreplace) %{_sysconfdir}/isoftapp/isoftapp.conf
%config(noreplace) %{_sysconfdir}/isoftapp/preferences
%config(noreplace) %{_sysconfdir}/isoftapp/rpmpriorities
%config(noreplace) %{_sysconfdir}/isoftapp/sources.list
%config(noreplace) %{_sysconfdir}/isoftapp/vendors.list
%dir %{_sysconfdir}/isoftapp/isoftapp.conf.d/
# NOTE: no noreplace because we WANT to be able to change the defaults
# without user intervention!
%config %{_sysconfdir}/isoftapp/isoftapp.conf.d/default.conf
%dir %{_sysconfdir}/isoftapp/sources.list.d/
%dir %{_sysconfdir}/isoftapp/vendors.list.d/
%{_bindir}/isoftapp
%{_libdir}/isoftapp/
%dir %{_datadir}/isoftapp/
%dir %{_datadir}/isoftapp/scripts/
%{_localstatedir}/cache/isoftapp/
%{_localstatedir}/lib/isoftapp/

%files devel
%{_includedir}/apt-pkg/
%{_libdir}/libapt-pkg*.so
%{_libdir}/pkgconfig/libapt-pkg.pc

%if 0%{!?_without_list:1}
%files plugins-list
%config %{_sysconfdir}/apt/apt.conf.d/list-extras.conf
%config %{_sysconfdir}/apt/apt.conf.d/list-nodeps.conf
%{_datadir}/apt/scripts/list-extras.lua
%{_datadir}/apt/scripts/list-nodeps.lua
%endif

%if 0%{!?_without_log:1}
%files plugins-log
%config %{_sysconfdir}/apt/apt.conf.d/log.conf
%{_datadir}/apt/scripts/log.lua
%endif


%changelog
* Wed Nov 18 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Fix isoftapp install/remove issue by fujiang.
- Fix isoftapp conf sources.list issue by fujiang.

* Sun Nov 08 2015 Cjacker <cjacker@foxmail.com> - 0.5.15lorg3.95-25.git522
- Seperate isoftapp package, use own config files

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 0.5.15lorg3.95-23.git522
- enable static build apt-get with isoftapp support, do not affect original apt

* Mon Nov 02 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Restore original seperate patches of lua and others.
- Apply isoftapp based on them.

* Fri Oct 30 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add iSOFT App skeleton implemented by fujiang and Leslie Zhai.

* Fri Oct 23 2015 cjacker - 0.5.15lorg3.95-20.git522
- Rebuild for new 4.0 release

