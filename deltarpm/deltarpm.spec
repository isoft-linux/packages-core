%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global with_python3 1

Summary: Create deltas between rpms
Name: deltarpm
Version: 3.6
Release: 10%{?dist}
License: BSD
Group: System Environment/Base
URL: http://gitorious.org/deltarpm/deltarpm
Source: ftp://ftp.suse.com/pub/projects/deltarpm/%{name}-%{version}.tar.bz2
Patch1: 0002-do-not-finish-applydeltarpm-jobs-when-in-the-middle-.patch
Patch2: 0003-add-newline-in-missing-prelink-error.patch
Patch3: 0004-Return-error-rather-than-crashing-if-we-can-t-alloca.patch 
Patch4: 0005-fix-off-by-one-error-in-delta-generation-code.patch
Patch5: 0006-Add-fflush-s-so-output-can-be-watched-using-tail-f.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, xz-devel, librpm-devel, popt-devel
BuildRequires: zlib-devel
BuildRequires: python-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary: Sync a file tree with deltarpms
Group: System Environment/Base
Requires: deltarpm%{_isa} = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary: Create deltas between isos containing rpms
Group: System Environment/Base
Requires: deltarpm%{_isa} = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python-deltarpm
Summary: Python bindings for deltarpm
Group: System Environment/Base
Requires: deltarpm%{_isa} = %{version}-%{release}

%description -n python-deltarpm
This package contains python bindings for deltarpm.

%if 0%{?with_python3}
%package -n python3-deltarpm
Summary: Python bindings for deltarpm
Group: System Environment/Base
Requires: deltarpm%{_isa} = %{version}-%{release}

%description -n python3-deltarpm
This package contains python bindings for deltarpm.
%endif


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%{__rm} -rf %{buildroot}
%makeinstall pylibprefix=%{buildroot}

%if 0%{?with_python3}
# nothing to do
%else
rm -rf %{buildroot}%{_libdir}/python3*
%endif


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltarpm*
%doc %{_mandir}/man8/makedeltarpm*
%doc %{_mandir}/man8/combinedeltarpm*
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%files -n deltaiso
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltaiso*
%doc %{_mandir}/man8/makedeltaiso*
%doc %{_mandir}/man8/fragiso*
%{_bindir}/applydeltaiso
%{_bindir}/fragiso
%{_bindir}/makedeltaiso

%files -n drpmsync
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/drpmsync*
%{_bindir}/drpmsync

%files -n python-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python_sitearch}/*

%if 0%{?with_python3}

%files -n python3-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python3_sitearch}/*

%endif

%changelog
* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- first build
