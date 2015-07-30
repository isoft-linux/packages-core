Name: docbook-style-xsl
Version: 1.74.0
Release: 4
Group:   CoreDev/Development/Utility/Documentation

Summary: Norman Walsh's XSL stylesheets for DocBook XML

License: Freely redistributable without restriction
URL: http://docbook.sourceforge.net/projects/xsl/

Provides: docbook-xsl = %{version}
Requires: docbook-dtd-xml
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3-8
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
# PassiveTeX before 1.21 can't handle the newer stylesheets.
Conflicts: passivetex < 1.21

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Source0: http://downloads.sourceforge.net/docbook/docbook-xsl-%{version}.tar.gz
Source1: %{name}.Makefile
Source2: http://downloads.sourceforge.net/docbook/docbook-xsl-doc-%{version}.tar.bz2

Patch1: docbook-xsl-pagesetup.patch
Patch2: docbook-xsl-marginleft.patch
Patch3: docbook-xsl-newmethods.patch
Patch4: docbook-xsl-non-constant-expressions.patch
Patch5: docbook-xsl-list-item-body.patch
Patch6: docbook-xsl-weird-orgname-use.patch


%description
These XSL stylesheets allow you to transform any DocBook XML document to
other formats, such as HTML, FO, and XHMTL.  They are highly customizable.


%prep
%setup -q -n docbook-xsl-%{version}
pushd ..
tar jxf %{SOURCE2}
popd
%patch1 -p1 -b .pagesetup
%patch2 -p1 -b .marginleft
%patch3 -p1 -b .newmethods
%patch4 -p1 -b .nonconstant
%patch5 -p1 -b .listitembody
%patch6 -p1 -b .orgname

cp -p %{SOURCE1} Makefile

for f in $(find -name "*'*")
do
  mv -v "$f" $(echo "$f" | tr -d "'")
done


%build


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install BINDIR=$DESTDIR%{_bindir} DESTDIR=$DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
ln -s xsl-stylesheets-%{version} \
	$DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets

# Don't ship the extensions (bug #177256).
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-stylesheets/extensions/*


%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root,-)
%doc BUGS
%doc README
%doc TODO
%doc doc
%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-stylesheets


%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl/current" \
 "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG


%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-stylesheets-%{version}" $CATALOG
fi

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

