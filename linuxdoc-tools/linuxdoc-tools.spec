%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global _vendorperllibdir %{_datadir}/perl5/vendor_perl

Summary: A text formatting package based on SGML
Name: linuxdoc-tools
Version: 0.9.68
Release: 9%{?dist}
License: Copyright only
Group: Applications/Publishing
Source: http://http.us.debian.org/debian/pool/main/l/linuxdoc-tools/%{name}_%{version}.tar.gz
Patch0: linuxdoc-tools-0.9.13-letter.patch
Patch1: linuxdoc-tools-0.9.20-lib64.patch
Patch2: linuxdoc-tools-0.9.68-flex.patch
Url: http://packages.qa.debian.org/l/linuxdoc-tools.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: flex sgml-common jade gawk groff autoconf texinfo
#need actual perl directory structure
BuildRequires: perl >= 4:5.10.1
Requires: jade gawk groff
Obsoletes: sgml-tools < %{version}-%{release}
Obsoletes: linuxdoc-sgml < %{version}-%{release}
Provides: sgml-tools = %{version}-%{release}
Provides: linuxdoc-sgml = %{version}-%{release}

%description
Linuxdoc-tools is a text formatting suite based on SGML (Standard
Generalized Markup Language), using the LinuxDoc document type.
Linuxdoc-tools allows you to produce LaTeX, HTML, GNU info, LyX, RTF,
plain text (via groff), and other format outputs from a single SGML
source.  Linuxdoc-tools is intended for writing technical software
documentation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .lib64
%patch2 -p1

%build
%configure --with-installed-iso-entities
# Packaging brain-damage
pushd entity-map
autoconf
%configure
popd

make OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           perl5lib/LinuxDocTools.pm

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_vendorperllibdir}
make install DESTDIR=$RPM_BUILD_ROOT perl5libdir=%{_vendorperllibdir}
[ $RPM_BUILD_ROOT%{_docdir}/%{name} = $RPM_BUILD_ROOT%{_pkgdocdir} ] \
           || mv $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_pkgdocdir}
perl -pi -e 's,/usr/share/sgml/iso-entities-8879.1986/iso-entities.cat,\$main::prefix/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           $RPM_BUILD_ROOT%{_vendorperllibdir}/LinuxDocTools.pm
#Copy license files for parts into docdir
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/sgmls-1.1
cp -p sgmls-1.1/LICENSE $RPM_BUILD_ROOT%{_pkgdocdir}/sgmls-1.1/LICENSE
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/iso-entities
cp -p iso-entities/COPYING $RPM_BUILD_ROOT%{_pkgdocdir}/iso-entities/COPYING
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/entity-map
cp -p entity-map/COPYING $RPM_BUILD_ROOT%{_pkgdocdir}/entity-map/COPYING
cp -p COPYING $RPM_BUILD_ROOT%{_pkgdocdir}/


# Some files need moving around.
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/epsf.*
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/url.sty
install -d $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/misc
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/*.sty \
  $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/misc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root,-)
%doc %{_pkgdocdir}
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%dir %{_vendorperllibdir}/Text
%{_vendorperllibdir}/Text/EntityMap.pm
%dir %{_vendorperllibdir}/LinuxDocTools
%{_vendorperllibdir}/LinuxDocTools.pm
%{_vendorperllibdir}/LinuxDocTools/*.pm
%{_mandir}/*/*

%changelog
