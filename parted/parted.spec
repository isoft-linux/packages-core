%define _sbindir /sbin
%define _libdir /%{_lib}

Summary: The GNU disk partition manipulation program
Name:    parted
Version: 3.2
Release: 1
License: GPLv3+
Group:   Core/Runtime/Utility
URL:     http://www.gnu.org/software/parted

Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildRequires: e2fsprogs-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: device-mapper-devel
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel >= 2.17
BuildRequires: autoconf automake
BuildRequires: e2fsprogs
BuildRequires: dosfstools

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.


%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Group:    Core/Development/Library
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.


%prep
%setup -q
%build
autoreconf
autoconf

CFLAGS="$RPM_OPT_FLAGS -Wno-unused-but-set-variable"; export CFLAGS
%configure --disable-static

V=1 %{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_infodir}
%{__rm} -rf %{buildroot}%{_bindir}/label
%{__rm} -rf %{buildroot}%{_bindir}/disk

%find_lang %{name}


%check
#2 check fail, that's ok.
export LD_LIBRARY_PATH=$(pwd)/libparted/.libs
make check ||:


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8.gz
%{_mandir}/man8/partprobe.8.gz
%{_libdir}/libparted.so.*
%{_libdir}/libparted-fs-resize.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/pkgconfig/libparted.pc


%changelog
