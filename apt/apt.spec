%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define generate_rpmpriorities 0
%define comps %{_datadir}/comps/%{_build_arch}/comps.xml

%define aptver 0.5.15lorg3.95
%define snapver git522
%define srcver %{aptver}.%{snapver}

# This is disabled because
# A) it is broken and bitrotten
# B) fixing it involves swig and ain't no one got time for that
%global with_python 0

Summary: Debian's Advanced Packaging Tool with RPM support
Name: apt
Version: %{aptver}
Release: 21.%{snapver}
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

# fix build with gcc 4.7
Patch2: apt-0.5.15lorg3.95-gcc47.patch
# iSOFT App skeleton implemented by fujiang
Patch7: 0001-isoft-app-skeleton.patch

# TODO: verify the required minimum Python version
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
%if 0%{!?_with_groupinstall:1}
Obsoletes: %{name}-plugins-groupinstall < %{version}-%{release}
%endif
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

%package devel
Summary: Development files and documentation for APT's libapt-pkg
Requires: %{name} = %{version}-%{release}
Requires: librpm-devel
Requires: pkgconfig

%description devel
This package contains development files for developing with APT's
libapt-pkg package manipulation library, modified for RPM.

%package python
Summary: Python bindings for libapt-pkg
Requires: %{name} = %{version}-%{release}

%description python
The apt-python package contains a module which allows python programs
to access the APT library interface.

%package plugins-groupinstall
Summary: Additional commands to install and remove package groups
Requires: %{name} = %{version}-%{release}
Requires: rhpl
Requires: comps

%description plugins-groupinstall
This package adds four new commands to apt for installing, removing
and viewing groups of packages:
apt-cache groupnames
apt-cache showgroup <groupname> [<groupname2> ..]
apt-get groupinstall <groupname> [<groupname2> ..]
apt-get groupremove <groupname> [<groupname2> ..]

The group information is retrieved from comps.xml used by anaconda
(the system installer) and other package management tools of
RHL/RHEL/FC distributions.

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
%setup -q -n %{name}-%{srcver}
%patch2 -p1 -b .gcc47
%patch7 -p1 -b .isoftapp

install -pm 644 %{SOURCE19} comps2prio.xsl

# don't require python, lua etc because of stuff in doc/contrib
find contrib/ -type f | xargs chmod 0644

%build
CXXFLAGS="%{optflags} -DLUA_COMPAT_MODULE"

%configure --disable-dependency-tracking --disable-static

make %{?_smp_mflags}

%if 0%{?with_python}
make -C python %{?_smp_mflags} PYTHON="%{__python}"
python -O -c "import py_compile; py_compile.compile('python/apt.py')"
%endif

cp -p %{SOURCE5} rpmpriorities
%if %{generate_rpmpriorities}
xsltproc -o rpmpriorities comps2prio.xsl %{comps}
%endif


%install
make install DESTDIR=%{buildroot} includedir=%{_includedir}/apt-pkg
%find_lang %{name}

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

%if 0%{?with_python}
# The python bindings
mkdir -p %{buildroot}%{python_sitearch}/
install -pm 755 python/_apt.so %{buildroot}%{python_sitearch}/
install -pm 644 python/apt.py* %{buildroot}%{python_sitearch}/
touch %{buildroot}%{python_sitearch}/apt.pyo
%endif

# apt-plugins-groupinstall from contrib
%if 0%{?_with_groupinstall:1}
install -pm 755 contrib/apt-groupinstall/{groupinstall-backend-comps.py,apt-groupinstall.lua} %{buildroot}/%{_datadir}/apt/scripts
touch %{buildroot}%{_datadir}/apt/scripts/groupinstall-backend-comps.py{c,o}
install -pm 644 contrib/apt-groupinstall/apt-groupinstall.conf \
 %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
%endif

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

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS* COPYING* ABOUT* TODO comps2prio.xsl doc/examples/ contrib/
%doc ChangeLog

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

%files devel
%{_includedir}/apt-pkg/
%{_libdir}/libapt-pkg*.so
%{_libdir}/pkgconfig/libapt-pkg.pc

%if 0%{?with_python}
%files python
%{python_sitearch}/_apt.so
%{python_sitearch}/apt.py*
%endif

%if 0%{?_with_groupinstall:1}
%files plugins-groupinstall
# XXX not config?
%{_sysconfdir}/apt/apt.conf.d/apt-groupinstall.conf
%{_datadir}/apt/scripts/apt-groupinstall.lua
%{_datadir}/apt/scripts/groupinstall-backend-comps.py
%ghost %{_datadir}/apt/scripts/groupinstall-backend-comps.py[co]
%endif

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
* Fri Oct 30 2015 Leslie Zhai <xiang.zhai@i-soft.com.cn>
- Add iSOFT App skeleton implemented by fujiang and Leslie Zhai.

* Fri Oct 23 2015 cjacker - 0.5.15lorg3.95-20.git522
- Rebuild for new 4.0 release

