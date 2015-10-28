Summary: A garbage collector for C and C++ 
Name:    gc	
Version: 7.4.2
Release: 2
License: BSD
Url:     http://www.hpl.hp.com/personal/Hans_Boehm/gc/	
Source0: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-%{version}.tar.gz
Source1: http://www.hpl.hp.com/research/linux/atomic_ops/download/libatomic_ops-7.4.0.tar.gz

BuildRequires: automake libtool 
BuildRequires: pkgconfig

# rpmforge compatibility
Obsoletes: libgc < %{version}-%{release}
Provides:  libgc = %{version}-%{release}

%description
The Boehm-Demers-Weiser conservative garbage collector can be 
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary: Libraries and header files for %{name} development 
Requires: %{name} = %{version}-%{release}
Obsoletes: libgc-devel < %{version}-%{release}
Provides:  libgc-devel = %{version}-%{release}
%description devel
%{summary}.

%package -n libatomic_ops-devel
Summary:   Atomic memory update operations
Provides:  libatomic_ops-static = %{version}-%{release}
%description -n libatomic_ops-devel 
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.


%prep
%setup -q -n gc-%{version} -a1
ln -s libatomic_ops-7.4.0 libatomic_ops

%build
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --enable-cplusplus \
  --enable-large-config \
%ifarch %{ix86}
  --enable-parallel-mark \
%endif
  --enable-threads=posix \
  --with-libatomic-ops=no

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} 
make install DESTDIR=%{buildroot} -C libatomic_ops 

install -p -D -m644 doc/gc.man	%{buildroot}%{_mandir}/man3/gc.3


%check
make check


%clean
rm -rf %{buildroot}


%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%{_libdir}/libcord.so.1*
%{_libdir}/libgc.so.1*
%{_libdir}/libgccpp.so.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gc.h
%{_includedir}/gc_cpp.h
%{_includedir}/gc/
%{_libdir}/libcord.so
%{_libdir}/libgc.so
%{_libdir}/libgccpp.so
%{_libdir}/pkgconfig/bdw-gc.pc
%{_mandir}/man3/gc.3*
%{_datadir}/gc

%files -n libatomic_ops-devel
%defattr(-,root,root,-)
%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a
%{_libdir}/pkgconfig/atomic_ops.pc
%dir %{_datadir}/libatomic_ops
%{_datadir}/libatomic_ops/*

%changelog
* Fri Oct 23 2015 cjacker - 7.4.2-2
- Rebuild for new 4.0 release

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

