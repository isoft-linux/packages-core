Summary: Integer point manipulation library
Name: isl
Version: 0.14
License: MIT
Group: System Environment/Libraries
URL: http://isl.gforge.inria.fr/

%global libmajor 13
%global libversion %{libmajor}.1.0

Release: 4%{?buildid}%{?dist}

BuildRequires: gmp-devel
BuildRequires: pkgconfig

Source0: http://isl.gforge.inria.fr/isl-%{version}.tar.xz

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%package devel
Summary: Development for building integer point manipulation library
Requires: isl%{?_isa} == %{version}-%{release}
Requires: gmp-devel%{?_isa}
Group: Development/Libraries

%description devel
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}/%{_libdir}/libisl.a
rm -f %{buildroot}/%{_libdir}/libisl.la
mkdir -p %{buildroot}/%{_datadir}
%global gdbprettydir %{_datadir}/gdb/auto-load/%{_libdir}
mkdir -p %{buildroot}/%{gdbprettydir}
mv %{buildroot}/%{_libdir}/*-gdb.py* %{buildroot}/%{gdbprettydir}

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libisl.so.%{libmajor}
%{_libdir}/libisl.so.%{libversion}
%{gdbprettydir}/*
%doc AUTHORS ChangeLog LICENSE README

%files devel
%{_includedir}/*
%{_libdir}/libisl.so
%{_libdir}/pkgconfig/isl.pc
%doc doc/manual.pdf


%changelog
* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- initial build.
