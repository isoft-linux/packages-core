Name:		    scons
Version:	    2.3.5
Release:	    1
Summary:	    An Open Source software construction tool
Group:		    Development/Tools
License:	    MIT
URL:		    http://www.scons.org
Source:		    http://downloads.sourceforge.net/scons/scons-%{version}.tar.gz
BuildArch:	    noarch

BuildRequires:	python-devel

%description
SCons is an Open Source software construction tool--that is, a build
tool; an improved substitute for the classic Make utility; a better way
to build software.  SCons is based on the design which won the Software
Carpentry build tool design competition in August 2000.

SCons "configuration files" are Python scripts, eliminating the need
to learn a new build tool syntax.  SCons maintains a global view of
all dependencies in a tree, and can scan source (or other) files for
implicit dependencies, such as files specified on #include lines.  SCons
uses MD5 signatures to rebuild only when the contents of a file have
really changed, not just when the timestamp has been touched.  SCons
supports side-by-side variant builds, and is easily extended with user-
defined Builder and/or Scanner objects.

%prep
%setup -q
%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install -O1 --skip-build \
    --root=%{buildroot} \
    --no-version-script \
	--standalone-lib \
    --install-scripts=%{_bindir} \
    --install-data=%{_datadir}
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt RELEASE.txt
%{_bindir}/*
%{_prefix}/lib/scons
%{_mandir}/man?/*

%changelog
