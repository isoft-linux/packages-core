%global with_python3 1

Summary: A utility for determining file types
Name: file
Version: 5.23
Release: 19
License: BSD
Group:  Core/Runtime/Utility 
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/
Requires: file-libs = %{version}-%{release}
BuildRequires: zlib-devel

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

%package libs
Summary: Libraries for applications using libmagic
Group:   Core/Runtime/Library 
License: BSD

%description libs

Libraries for applications using libmagic.

%package devel
Summary:  Libraries and header files for file development
Group:    Core/Deveopment/Library
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%package static
Summary: Static library for file development
Group:   Core/Development/Library 
Requires: %{name} = %{version}-%{release}

%description static
The file-static package contains the static version of
the libmagic library.


%package -n python-magic
Summary: Python 2 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python2-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python-magic
This package contains the Python 2 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%if %{with_python3}
%package -n python3-magic
Summary: Python 3 bindings for the libmagic API
Group:   Development/Libraries
BuildRequires: python3-devel
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n python3-magic
This package contains the Python 3 bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.
%endif


%prep
%setup -q

%if %{with_python3}
rm -rf %{py3dir}
cp -a python %{py3dir}
%endif


%build
%configure 
make %{?_smp_mflags}

cd python
CFLAGS="%{optflags}" %{__python} setup.py build
%if %{with_python3}
cd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
%endif


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install


cd python
%{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%if %{with_python3}
cd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%endif


rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*so.*
%{_datadir}/misc/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/magic.h
%{_mandir}/man3/*


%files -n python-magic
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc python/README python/example.py
%{python_sitelib}/magic.py
%{python_sitelib}/magic.pyc
%{python_sitelib}/magic.pyo
%{python_sitelib}/*egg-info

%if %{with_python3}
%files -n python3-magic
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc python/README python/example.py
%{python3_sitelib}/magic.py
%{python3_sitelib}/*egg-info
%{python3_sitelib}/__pycache__/magic*.pyc
%{python3_sitelib}/__pycache__/magic*.pyo
%endif


%changelog
