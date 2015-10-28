%define pkg docbook-slides
Summary: DocBook Slides document type and stylesheets
Name: docbook-slides
Version: 3.4.0
Release: 17%{?dist}
License: MIT
URL: http://sourceforge.net/projects/docbook
Source0: http://downloads.sourceforge.net/docbook/%{name}-%{version}.tar.gz
Source1: %{name}.xml
Source2: %{name}.cat
Source3: %{name}.README.redhat
#tests update and buildtools could be downloaded at upstream svn ... e.g.
#http://docbook.svn.sourceforge.net/viewvc/docbook/trunk/slides/tests/
Source4: %{name}-tests.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: docbook-dtds
Requires: docbook-xsl
Requires: docbook-simple
Requires: sgml-common
Requires(post): sed
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8


%description
DocBook Slides provides customization layers of the both the
Simplified and the full DocBook XML DTD, as well as the DocBook XSL
Stylesheets. This package contains the XML document type definition
and stylesheets for processing DocBook Slides XML. The slides doctype
and stylesheets are for generating presentations, primarily in HTML.

%prep
%setup -q -n %{pkg}-%{version}
tar xf %{SOURCE4}

%build

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT%{_datadir}/xml/docbook/slides/%{version}
mkdir -p $DESTDIR
cp -a browser $DESTDIR
cp -a graphics $DESTDIR
cp -a schema $DESTDIR
cp -a xsl $DESTDIR
cp -a VERSION $DESTDIR
cp -a catalog.xml $DESTDIR

## Install package catalogs into /etc/*ml/ ##

XML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xml
mkdir -p $XML_CAT_DIR
install -p -m 644 %{SOURCE1} $XML_CAT_DIR

SGML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/sgml
mkdir -p $SGML_CAT_DIR
install -p -m 644 %{SOURCE2} $SGML_CAT_DIR

cp -p %{SOURCE3} ./README2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root, -)
%doc doc
%doc tests
%doc README
%doc NEWS
%doc README2
%dir %{_datadir}/xml/docbook/slides/
%{_datadir}/xml/docbook/slides/%{version}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook-slides.cat
%config(noreplace) %{_sysconfdir}/xml/docbook-slides.xml


%post

##################  XML catalog registration #######################

## Define handy variables ##

ROOT_XML_CATALOG=%{_sysconfdir}/xml/catalog
PKG_XML_CATALOG=%{_sysconfdir}/xml/docbook-slides.xml
#LOCAL_XML_CATALOG=/usr/share/xml/docbook/slides/3.4.0/catalog.xml

#
# Register it in the super catalog with the appropriate delegates
#
if [ -w $ROOTCATALOG ]
then
        %{_bindir}/xmlcatalog --noout --add "delegatePublic" \
                "-//Norman Walsh//DTD Slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

        %{_bindir}/xmlcatalog --noout --add "delegateSystem" \
                "http://docbook.sourceforge.net/release/slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
        %{_bindir}/xmlcatalog --noout --add "delegateURI" \
                "http://docbook.sourceforge.net/release/slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
fi
####################################################################


#################  SGML catalog registration  ######################

ROOT_SGML_CATALOG=%{_sysconfdir}/sgml/catalog
PKG_SGML_CATALOG=%{_sysconfdir}/sgml/docbook-slides.cat

#### Root SGML Catalog Entries ####
#### "Delegate" appropriate lookups to package catalog ####

############## use install-catalog ######################

if [ -w $ROOT_SGML_CATALOG ]
then
# xmlcatalog deletes OVERRIDE YES directive, use install-catalog instead
#         /usr/bin/xmlcatalog --sgml --noout --add \
#     "/etc/sgml/docbook-slides.cat"

  install-catalog --add \
  $PKG_SGML_CATALOG \
  $ROOT_SGML_CATALOG 1>/dev/null

# Hack to workaround bug in install-catalog
  sed -i '/^CATALOG.*log\"$/d' $PKG_SGML_CATALOG
  sed -i '/^CATALOG.*log$/d' $PKG_SGML_CATALOG
fi

####################################################################

# Finally, make sure everything in /etc/*ml is readable!
/bin/chmod a+r %{_sysconfdir}/sgml/*
/bin/chmod a+r %{_sysconfdir}/xml/*

%postun
##
## SGML and XML catalogs
##
## Jobs: remove package catalog entries from both root catalogs &
##       remove package catalogs

# remove catalog entries only on removal of package
if [ "$1" = 0 ]; then
  %{_bindir}/xmlcatalog --sgml --noout --del \
    %{_sysconfdir}/sgml/catalog \
    "%{_sysconfdir}/sgml/docbook-slides.cat"

  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_sysconfdir}/xml/docbook-slides.xml" \
    %{_sysconfdir}/xml/catalog
fi

%changelog
* Fri Oct 23 2015 cjacker - 3.4.0-17
- Rebuild for new 4.0 release

