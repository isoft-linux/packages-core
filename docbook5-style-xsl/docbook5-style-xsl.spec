Name: docbook5-style-xsl
Version: 1.78.1
Release: 8%{?dist}

Summary: Norman Walsh's XSL stylesheets for DocBook 5.X

# Package is licensed as MIT/X (http://wiki.docbook.org/topic/DocBookLicense),
# some .js files under ./slides/browser/ are licensed MPLv1.1
License: MIT and MPLv1.1
URL: http://wiki.docbook.org/DocBookXslStylesheets

Provides: docbook-xsl-ns = %{version}
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3-8
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
Conflicts: passivetex < 1.21

BuildArch: noarch
Source0: http://downloads.sourceforge.net/docbook/docbook-xsl-ns-%{version}.tar.bz2

%description
These XSL namespace aware stylesheets allow you to transform any
DocBook 5 document to other formats, such as HTML, manpages, FO,
XHMTL and other formats. They are highly customizable. For more
information see W3C page about XSL.

#Don't ship Java extensions in Fedora as they are not compiled from the source
#Shiping sources instead of binary jars was requested by
#https://lists.oasis-open.org/archives/docbook-apps/201408/msg00008.html
#Sources available in the docbook stylesheets svn repository, but not packaged.
%if 0%{?rhel} >= 7
%package extensions
Summary: Norman Walsh's XSL stylesheets extensions for DocBook 5.X
# Package is licensed as MIT/X (http://wiki.docbook.org/topic/DocBookLicense),
# some .js files under ./slides/browser/ are licensed MPLv1.1
License: MIT and ASL 2.0
Requires: docbook-xsl-ns = %{version}

%description extensions
This package contains Java extensions for XSL namespace aware stylesheets.
%endif

%prep
%setup -q -n docbook-xsl-ns-%{version}
#remove .gitignore files
rm -rf $(find -name '.gitignore' -type f)
#make ruby scripts executable
chmod +x epub/bin/dbtoepub

%build

%install
DESTDIR=$RPM_BUILD_ROOT
mkdir -p $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version
cp -a [[:lower:]]* $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/
cp -a VERSION $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION.xsl
ln -s VERSION.xsl \
$DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION
ln -s xsl-ns-stylesheets-%{version} \
 $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets

# Don't ship install shell script.
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets/install.sh

%files
%defattr (-,root,root,-)
%doc BUGS
%doc README COPYING
%doc TODO NEWS
%doc RELEASE-NOTES.*
%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-ns-stylesheets
%exclude %{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}/extensions

%if 0%{?rhel} >= 7
%files extensions
%doc extensions/README.txt extensions/LICENSE.txt
%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}/extensions
%endif

%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl-ns/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl-ns/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG


%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
fi

%changelog
* Fri Oct 23 2015 cjacker - 1.78.1-8
- Rebuild for new 4.0 release

