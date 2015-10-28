Name: docbook-simple
Version: 1.1
Release: 16%{?dist}
Summary: Simplified DocBook is a small subset of the DocBook XML DTD
License: Freely redistributable without restriction
URL: http://www.oasis-open.org/docbook/xml/simple/
Source0: http://www.docbook.org/xml/simple/1.1/%{name}-%{version}.zip
Source1: %{name}.README.redhat
Source2: %{name}.xml
Source3: %{name}.cat
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: unzip
Requires: sgml-common
Requires(post): sed
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
Requires: docbook-dtds

%description
Simplified DocBook is an attempt to provide a proper subset of DocBook
that is simultaneously smaller and still useful. Documents written in
the subset must be 100% legal DocBook documents. This is a subset for
single documents (articles, white papers, etc.), so there's no need
for books or sets, just 'articles'. Simplified DocBook documents are 
viewable in online browsers if styled with CSS. (it's XML not SGML).


%prep
# splatter the files into a version-numbered directory
%setup -q -c -n %{version}

# see http://rpm-devel.colug.net/max-rpm/s1-rpm-inside-macros.html
# setup -c creates the dir then changes to it to expand SOURCE0

%build

%install

rm -rf $RPM_BUILD_ROOT

########## install versioned-numbered directory of dtd files ############

DESTDIR=$RPM_BUILD_ROOT%{_datadir}/xml/docbook/simple
mkdir -p $DESTDIR
cp -a ../%{version} $DESTDIR

########## install package catalogs  ################

XML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xml
mkdir -p $XML_CAT_DIR
install -p -m 644 %{SOURCE2} $XML_CAT_DIR

SGML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/sgml
mkdir -p $SGML_CAT_DIR
install -p -m 644 %{SOURCE3} $SGML_CAT_DIR

####### FIXME: must copy README.redhat to source directory ########
#######        for %doc to find it, ${SOURCE1} doesn't work ########

cp -p %{SOURCE1} ./README

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf ../%{version}

%files
%defattr (-,root,root,-)
%doc sdocbook.css
%doc README
%dir %{_datadir}/xml/docbook/simple/
%{_datadir}/xml/docbook/simple/%{version}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook-simple.cat
%config(noreplace) %{_sysconfdir}/xml/docbook-simple.xml


%post

##################  XML catalog registration #######################

## Define handy variables ##

ROOT_XML_CATALOG=%{_sysconfdir}/xml/catalog
PKG_XML_CATALOG=%{_sysconfdir}/xml/docbook-simple.xml

#### Root XML Catalog Entries ####
#### Delegate appropriate lookups to package catalog ####

if [ -w $ROOT_XML_CATALOG ]
then
        %{_bindir}/xmlcatalog --noout --add "delegatePublic" \
                "-//OASIS//DTD Simplified" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

        %{_bindir}/xmlcatalog --noout --add "delegateURI" \
                "http://www.oasis-open.org/docbook/xml/simple/1.1/" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

  # Next line because some resolvers misinterpret uri entries
        %{_bindir}/xmlcatalog --noout --add "delegateSystem" \
                "http://www.oasis-open.org/docbook/xml/simple/1.1/" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
fi

####################################################################


#################  SGML catalog registration  ######################

ROOT_SGML_CATALOG=%{_sysconfdir}/sgml/catalog
PKG_SGML_CATALOG=%{_sysconfdir}/sgml/docbook-simple.cat

#### Root SGML Catalog Entries ####
#### "Delegate" appropriate lookups to package catalog ####


############## use install-catalog ######################

if [ -w $ROOT_SGML_CATALOG ]
then
# xmlcatalog deletes OVERRIDE YES directive, use install-catalog instead
#         /usr/bin/xmlcatalog --sgml --noout --add \
#     "/etc/sgml/docbook-simple.cat"

  install-catalog --add \
  "$PKG_SGML_CATALOG" \
  "$ROOT_SGML_CATALOG" 1>/dev/null

# Hack to workaround bug in install-catalog
  sed -i '/^CATALOG.*log\"$/d' $PKG_SGML_CATALOG
  sed -i '/^CATALOG.*log$/d' $PKG_SGML_CATALOG   
fi

####################################################################


# Finally, make sure everything in /etc/*ml is readable!
/bin/chmod a+r  %{_sysconfdir}/sgml/*
/bin/chmod a+r  %{_sysconfdir}/xml/*

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
     %{_sysconfdir}/sgml/docbook-simple.cat

  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_sysconfdir}/xml/docbook-simple.xml" \
     %{_sysconfdir}/xml/catalog 
fi

%changelog
* Fri Oct 23 2015 cjacker - 1.1-16
- Rebuild for new 4.0 release

