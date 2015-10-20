%{!?tcl:%define tcl 0}
%{!?guile:%define guile 0}

Summary: Connects C/C++/Objective C to some high-level programming languages.
Name: swig
Version: 3.0.7
Release: 1
License: BSD
Group: CoreDev/Development/Utility
URL: http://swig.sourceforge.net/
Source: http://downloads.sourceforge.net/project/swig/swig/swig-%{version}/swig-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl, python-devel
%if %{tcl}
BuildRequires: tcl-devel
%endif
%if %{guile}
BuildRequires: guile-devel
%endif
BuildRequires: autoconf, automake, gawk

%description
Simplified Wrapper and Interface Generator (SWIG) is a software
development tool for connecting C, C++ and Objective C programs with a
variety of high-level programming languages.  SWIG is primarily used
with Perl, Python and Tcl/TK, but it has also been extended to Java,
Eiffel and Guile.  SWIG is normally used to create high-level
interpreted programming environments, systems integration, and as a
tool for building user interfaces.

%prep
%setup -q -n swig-%{version}
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} `perl -p -e 's|\S+%{_docdir}/%{name}-doc-%{version}\S+||'`
EOF

%define __perl_provides %{_builddir}/%{name}-%{version}/%{name}-prov
chmod +x %{__perl_provides}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} `perl -p -e 's|\S+%{_docdir}/%{name}-doc-%{version}\S+||'`
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
./autogen.sh
%configure
make %{?_smp_mflags}
#make check

%install
rm -rf $RPM_BUILD_ROOT

# Remove all arch dependent files in Examples/
pushd Examples/
for all in `find Makefile.in`; do
    rm -f "${all%%.in}"
done
popd

make DESTDIR=$RPM_BUILD_ROOT install
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/swig
%{_mandir}/man1/ccache-swig.1*

%changelog
* Sat Oct 10 2015 Cjacker <cjacker@foxmail.com>
- update to 3.0.7
