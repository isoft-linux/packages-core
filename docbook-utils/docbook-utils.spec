Name: docbook-utils
Version: 0.6.14
Release: 40%{?dist}

Summary: Shell scripts for managing DocBook documents
URL: http://sources.redhat.com/docbook-tools/

License: GPLv2+

Requires: docbook-style-dsssl >= 1.72
Requires: docbook-dtds
Requires: perl-SGMLSpm >= 1.03ii
Requires: which grep gawk
Requires: text-www-browser

BuildRequires: perl-SGMLSpm, openjade, docbook-style-dsssl

BuildArch: noarch
Source0: ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tar.gz
Source1: db2html
Source2: gdp-both.dsl
#We will ship newer version of docbook2man-spec.pl for better handling of docbook2man conversion
#You could check it at http://sourceforge.net/projects/docbook2x/
Source3: docbook2man-spec.pl

Obsoletes: stylesheets < %{version}-%{release}
Provides: stylesheets = %{version}-%{release}

Patch0: docbook-utils-spaces.patch
Patch1: docbook-utils-2ndspaces.patch
Patch2: docbook-utils-w3mtxtconvert.patch
Patch3: docbook-utils-grepnocolors.patch
Patch4: docbook-utils-sgmlinclude.patch
Patch5: docbook-utils-rtfmanpage.patch
Patch6: docbook-utils-papersize.patch
Patch7: docbook-utils-nofinalecho.patch
Patch8: docbook-utils-newgrep.patch

%description
This package contains scripts are for easy conversion from DocBook
files to other formats (for example, HTML, RTF, and PostScript), and
for comparing SGML files.

#%package pdf
#Requires: jadetex >= 2.5
#Requires: docbook-utils = %{version}
#Requires: tex(dvips)
#Requires: texlive-collection-fontsrecommended
#Requires: texlive-collection-htmlxml
#License: GPL+
#Group: Applications/Text
#Obsoletes: stylesheets-db2pdf <= %{version}-%{release}
#Provides: stylesheets-db2pdf = %{version}-%{release}
#Summary: A script for converting DocBook documents to PDF format
#URL: http://sources.redhat.com/docbook-tools/
#
#%description pdf
#This package contains a script for converting DocBook documents to
#PDF format.

%prep
%setup -q
%patch0 -p1 -b .spaces
%patch1 -p1 -b .2ndspaces
%patch2 -p1 -b .w3mtxtconvert
%patch3 -p1 -b .grepnocolors
%patch4 -p1 -b .sgmlinclude
%patch5 -p1 -b .rtfman
%patch6 -p1 -b .papersize
%patch7 -p1 -b .finalecho
%patch8 -p1 -b .newgrep

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir} --libdir=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
make install prefix=%{_prefix} mandir=%{_mandir} docdir=/tmp
for util in dvi html pdf ps rtf
do
	ln -s docbook2$util $RPM_BUILD_ROOT%{_bindir}/db2$util
	ln -s jw.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/db2$util.1
done
ln -s jw.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/docbook2txt.1
# db2html is not just a symlink, as it has to create the output directory
rm -f $RPM_BUILD_ROOT%{_bindir}/db2html
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/db2html
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/utils-%{version}/docbook-utils.dsl
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/utils-%{version}/helpers/docbook2man-spec.pl

rm -rf $RPM_BUILD_ROOT/tmp

%clean

%files
%defattr (-,root,root,-)
%doc README COPYING TODO
%{_bindir}/jw
%{_bindir}/docbook2html
%{_bindir}/docbook2man
%{_bindir}/docbook2rtf
%{_bindir}/docbook2tex
%{_bindir}/docbook2texi
%{_bindir}/docbook2txt
%attr(0755,root,root) %{_bindir}/db2html
%{_bindir}/db2rtf
%{_bindir}/sgmldiff
%{_datadir}/sgml/docbook/utils-%{version}
%{_mandir}/*/db2dvi.*
%{_mandir}/*/db2html.*
%{_mandir}/*/db2ps.*
%{_mandir}/*/db2rtf.*
%{_mandir}/*/docbook2html.*
%{_mandir}/*/docbook2rtf.*
%{_mandir}/*/docbook2man.*
%{_mandir}/*/docbook2tex.*
%{_mandir}/*/docbook2texi.*
%{_mandir}/*/docbook2txt.*
%{_mandir}/*/jw.*
%{_mandir}/*/sgmldiff.*
%{_mandir}/*/*-spec.*

#%files pdf
#%defattr (-,root,root,-)
#%{_bindir}/docbook2pdf
#%{_bindir}/docbook2dvi
#%{_bindir}/docbook2ps
#%{_bindir}/db2dvi
#%{_bindir}/db2pdf
#%{_bindir}/db2ps
#%{_mandir}/*/db2pdf.*
#%{_mandir}/*/docbook2pdf.*
#%{_mandir}/*/docbook2dvi.*
#%{_mandir}/*/docbook2ps.*

%changelog
* Fri Oct 23 2015 cjacker - 0.6.14-40
- Rebuild for new 4.0 release

