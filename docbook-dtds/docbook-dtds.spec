%define openjadever 1.3.2

Name: docbook-dtds
Version: 1.0
Release: 41
Group:  CoreDev/Development/Utility/Documentation 

Summary: SGML and XML document type definitions for DocBook

License: Freely redistributable without restriction
URL: http://www.oasis-open.org/docbook/

Obsoletes: docbook-dtd30-sgml <= %{version}-%{release}
Obsoletes: docbook-dtd31-sgml <= %{version}-%{release}
Obsoletes: docbook-dtd40-sgml <= %{version}-%{release}
Obsoletes: docbook-dtd41-sgml <= %{version}-%{release}
Obsoletes: docbook-dtd412-xml <= %{version}-%{release}

Provides: docbook-dtd-xml = %{version}-%{release} 
Provides: docbook-dtd-sgml = %{version}-%{release}
Provides: docbook-dtd30-sgml = %{version}-%{release}
Provides: docbook-dtd31-sgml = %{version}-%{release}
Provides: docbook-dtd40-sgml = %{version}-%{release} 
Provides: docbook-dtd41-sgml = %{version}-%{release}
Provides: docbook-dtd412-xml = %{version}-%{release}
Provides: docbook-dtd42-sgml = %{version}-%{release}
Provides: docbook-dtd42-xml = %{version}-%{release}
Provides: docbook-dtd43-sgml = %{version}-%{release}
Provides: docbook-dtd43-xml = %{version}-%{release}
Provides: docbook-dtd44-sgml = %{version}-%{release}
Provides: docbook-dtd44-xml = %{version}-%{release}
Provides: docbook-dtd45-sgml = %{version}-%{release}
Provides: docbook-dtd45-xml = %{version}-%{release}

Requires: grep perl
Requires(post): libxml2 >= 2.4.8
Requires(post): coreutils
Requires(postun): libxml2 >= 2.4.8
# If upgrading, the old package's postun scriptlet may use install-catalog
# to remove its entries.  xmlcatalog (which this package uses) adds quotes
# to the catalog files, and install-catalog only handles this in 0.6.3-4 or
# later.
Requires: sgml-common >= 0.6.3-4
# We provide the directory layout expected by 0.6.3-5 or later of
# xml-common.  Earlier versions won't understand. Additionally 
# require xml-common >= 0.6.3-24 to workaround issue with F9 
# install+update and empty xmlcatalog
Requires: xml-common >= 0.6.3-24

BuildRoot: %{_tmppath}/%{name}-%{version}

BuildArch: noarch
Source0: http://www.oasis-open.org/docbook/sgml/3.0/docbk30.zip
Source1: http://www.oasis-open.org/docbook/sgml/3.1/docbk31.zip
Source2: http://www.oasis-open.org/docbook/sgml/4.0/docbk40.zip
Source3: http://www.oasis-open.org/docbook/sgml/4.1/docbk41.zip
Source4: http://www.oasis-open.org/docbook/xml/4.1.2/docbkx412.zip
Source5: http://www.oasis-open.org/docbook/sgml/4.2/docbook-4.2.zip
Source6: http://www.oasis-open.org/docbook/xml/4.2/docbook-xml-4.2.zip
Source7: http://www.docbook.org/sgml/4.3/docbook-4.3.zip
Source8: http://www.docbook.org/xml/4.3/docbook-xml-4.3.zip
Source9: http://www.docbook.org/sgml/4.4/docbook-4.4.zip
Source10: http://www.docbook.org/xml/4.4/docbook-xml-4.4.zip
Source11: http://www.docbook.org/sgml/4.5/docbook-4.5.zip
Source12: http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip
Patch0: docbook-dtd30-sgml-1.0.catalog.patch
Patch1: docbook-dtd31-sgml-1.0.catalog.patch
Patch2: docbook-dtd40-sgml-1.0.catalog.patch
Patch3: docbook-dtd41-sgml-1.0.catalog.patch
Patch4: docbook-dtd42-sgml-1.0.catalog.patch
Patch5: docbook-4.2-euro.patch
Patch6: docbook-dtds-ents.patch
BuildRequires: unzip

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This package contains SGML and XML versions of the DocBook DTD. 


%prep
%setup -c -T
# DocBook V3.0
mkdir 3.0-sgml
cd 3.0-sgml
unzip %{SOURCE0}
patch -b docbook.cat %{PATCH0}
cd ..

# DocBook V3.1
mkdir 3.1-sgml
cd 3.1-sgml
unzip %{SOURCE1}
patch -b docbook.cat %{PATCH1}
cd ..

# DocBook V4.0
mkdir 4.0-sgml
cd 4.0-sgml
unzip %{SOURCE2}
patch -b docbook.cat %{PATCH2}
cd ..

# DocBook V4.1
mkdir 4.1-sgml
cd 4.1-sgml
unzip %{SOURCE3}
patch -b docbook.cat %{PATCH3}
cd ..

# DocBook XML V4.1.2
mkdir 4.1.2-xml
cd 4.1.2-xml
unzip %{SOURCE4}
cd ..

# DocBook V4.2
mkdir 4.2-sgml
cd 4.2-sgml
unzip %{SOURCE5}
patch -b docbook.cat %{PATCH4}
cd ..

# DocBook XML V4.2
mkdir 4.2-xml
cd 4.2-xml
unzip %{SOURCE6}
cd ..

# DocBook V4.3
mkdir 4.3-sgml
cd 4.3-sgml
unzip %{SOURCE7}
cd ..

# DocBook XML V4.3
mkdir 4.3-xml
cd 4.3-xml
unzip %{SOURCE8}
cd ..

# DocBook V4.4
mkdir 4.4-sgml
cd 4.4-sgml
unzip %{SOURCE9}
cd ..

# DocBook XML V4.4
mkdir 4.4-xml
cd 4.4-xml
unzip %{SOURCE10}
cd ..

# DocBook v4.5
mkdir 4.5-sgml
cd 4.5-sgml
unzip %{SOURCE11}
cd ..

# DocBook XML v4.5
mkdir 4.5-xml
cd 4.5-xml
unzip %{SOURCE12}
cd ..

# Fix &euro; in SGML.
%patch5 -p1

# Fix ISO entities in 4.3/4.4 SGML
%patch6 -p1

# Increase NAMELEN (bug #36058, bug #159382).
sed -e's,\(NAMELEN\s\+\)44\(\s\*\)\?,\1256,' -i.namelen */docbook.dcl

# fix of \r\n issue from rpmlint
sed -i 's/\r//' */*.txt


if [ `id -u` -eq 0 ]; then
  chown -R root:root .
  chmod -R a+rX,g-w,o-w .
fi


%build


%install
rm -rf $RPM_BUILD_ROOT

# DocBook V3.0
cd 3.0-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V3.1
cd 3.1-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V4.0
cd 4.0-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V4.1
cd 4.1-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.1.2
cd 4.1.2-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.2
cd 4.2-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.2
cd 4.2-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.3
cd 4.3-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.3
cd 4.3-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.4
cd 4.4-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.4
cd 4.4-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.5
cd 4.5-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.5-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.5
cd 4.5-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.5-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..


# Symlinks
mkdir -p $RPM_BUILD_ROOT/etc/sgml
ln -s sgml-docbook-4.5-%{version}-%{release}.cat \
  $RPM_BUILD_ROOT/etc/sgml/sgml-docbook.cat
ln -s xml-docbook-4.5-%{version}-%{release}.cat \
  $RPM_BUILD_ROOT/etc/sgml/xml-docbook.cat

# Files for %ghost
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat
touch $RPM_BUILD_ROOT/etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (0644,root,root,0755)
#in upstream tarballs there is a lot of files with 0755 permissions
#but they don't need to be, 0644 is enough for every file in tarball
%doc --parents 3.1-sgml/ChangeLog
%doc --parents 4.1-sgml/ChangeLog
%doc --parents */*.txt
%config(noreplace) /etc/sgml/sgml-docbook.cat
%config(noreplace) /etc/sgml/xml-docbook.cat
/usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.5-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.5-%{version}-%{release}
%ghost %config(noreplace) /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat
%ghost %config(noreplace) /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat

%post
## Clean up pre-docbook-dtds mess caused by broken trigger.
for v in 3.0 3.1 4.0 4.1 4.2
do
  if [ -f /etc/sgml/sgml-docbook-$v.cat ]
  then
    /usr/bin/xmlcatalog --sgml --noout --del \
      /etc/sgml/sgml-docbook-$v.cat \
      /usr/share/sgml/openjade-1.3.1/catalog 2>/dev/null
  fi
done

##
## SGML catalog
##

# Update the centralized catalog corresponding to this version of the DTD
# DocBook V3.0
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}/catalog

# DocBook V3.1
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}/catalog

# DocBook V4.0
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}/catalog

# DocBook V4.1
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}/catalog

# DocBook XML V4.1.2
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}/catalog

# DocBook V4.2
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}/catalog

# DocBook XML V4.2
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}/catalog

# DocBook V4.3
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}/catalog

# DocBook XML V4.3
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}/catalog

# DocBook V4.4
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}/catalog

# DocBook XML V4.4
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}/catalog

# DocBook V4.5
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/sgml-dtd-4.5-%{version}-%{release}/catalog

# DocBook XML V4.5
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/docbook/xml-dtd-4.5-%{version}-%{release}/catalog


# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
STYLESHEETS=$(echo /usr/share/sgml/docbook/dsssl-stylesheets-*)
STYLESHEETS=${STYLESHEETS##*/dsssl-stylesheets-}
if [ "$STYLESHEETS" != "*" ]; then
    # DocBook V3.0
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V3.1
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.0
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.1
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.1.2
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.2
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.2
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.3
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.3
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.4
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.4
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

   # DocBook V4.5
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.5
    /usr/bin/xmlcatalog --sgml --noout --add \
    /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat \
    /usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

fi

# Fix up SGML super catalog so that there isn't an XML DTD before an
# SGML one.  We need to do this (*sigh*) because xmlcatalog messes up
# the order of the lines, and SGML tools don't like to see XML things
# they aren't expecting.
CAT_DIR=/usr/share/sgml/docbook/
CATALOG=/etc/sgml/catalog
SGML=$(cat -n ${CATALOG} | grep sgml-docbook | head -1 | (read n line;echo $n))
XML=$(cat -n ${CATALOG} | grep xml-docbook | head -1 | (read n line; echo $n))
# Do they need switching around?
if [ -n "${XML}" ] && [ -n "${SGML}" ] && [ "${XML}" -lt "${SGML}" ]
then
  # Switch those two lines around.
  XML=$((XML - 1))
  SGML=$((SGML - 1))
  perl -e "@_=<>;@_[$XML, $SGML]=@_[$SGML, $XML];print @_" \
    ${CATALOG} > ${CATALOG}.rpmtmp
  mv -f ${CATALOG}.rpmtmp ${CATALOG}
fi

##
## XML catalog
##

CATALOG=/usr/share/sgml/docbook/xmlcatalog

if [ -w $CATALOG ]
then
  # DocBook XML V4.1.2
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.1.2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.1.2" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.1.2" \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}" $CATALOG

  # DocBook XML V4.2
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.2" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.2" \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}" $CATALOG

  # DocBook XML V4.3
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.3//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.3" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.3" \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}" $CATALOG

  # DocBook XML V4.4
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isopub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isobox.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isonum.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isodia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isocyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isotech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.4//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isolat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isolat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isocyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.4" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.4" \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}" $CATALOG

   # DocBook XML V4.5
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Publishing//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isopub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Letters//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isobox.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isonum.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isodia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isocyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES General Technical//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isotech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 1//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isolat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Latin 2//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isolat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "public" \
    "ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isocyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}" $CATALOG
  /usr/bin/xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}" $CATALOG

fi

# Finally, make sure everything in /etc/sgml is readable!
/bin/chmod a+r /etc/sgml/*

%triggerin -- openjade >= %{?openjadever}
#openjade catalog registration
  # DocBook V3.0
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V3.1
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.0
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
 
  # DocBook V4.1
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.1.2
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.2
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.2
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.3
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.3
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.4
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.4
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
 
  # DocBook V4.5
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.5
  /usr/bin/xmlcatalog --sgml --noout --add \
  /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
#openjade registration trigger end

%triggerun -- openjade >= %{?openjadever}
  [ $2 = 0 ] || exit 0
  #openjade catalog unregistration
  # DocBook V3.0
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V3.1
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.0
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
 
  # DocBook V4.1
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.1.2
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.2
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.2
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.3
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.3
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook V4.4
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.4
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
 
  # DocBook V4.5
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog

  # DocBook XML V4.5
  /usr/bin/xmlcatalog --sgml --noout --del \
  /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat \
  /usr/share/sgml/openjade-%{openjadever}/catalog
#openjade unregistration trigger end

 
%postun
##
## SGML catalog
##

# Update the centralized catalog corresponding to this version of the DTD
# DocBook V3.0
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat

# DocBook V3.1
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat

# DocBook V4.0
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat

# DocBook V4.1
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat

# DocBook XML V4.1.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat

# DocBook V4.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat

# DocBook XML V4.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat

# DocBook V4.3
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat

# DocBook XML V4.3
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat

# DocBook V4.4
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat

# DocBook XML V4.4
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat

# DocBook V4.5
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.5-%{version}-%{release}.cat

# DocBook XML V4.5
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
  /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.5-%{version}-%{release}.cat


# Fix up SGML super catalog so that there isn't an XML DTD before an
# SGML one.  We need to do this (*sigh*) because xmlcatalog messes up
# the order of the lines, and SGML tools don't like to see XML things
# they aren't expecting.
CATALOG=/etc/sgml/catalog
SGML=$(cat -n ${CATALOG} | grep sgml-docbook | head -1 | (read n line;echo $n))
XML=$(cat -n ${CATALOG} | grep xml-docbook | head -1 | (read n line; echo $n))
# Do they need switching around?
if [ -n "${XML}" ] && [ -n "${SGML}" ] && [ "${XML}" -lt "${SGML}" ]
then
  # Switch those two lines around.
  XML=$((XML - 1))
  SGML=$((SGML - 1))
  perl -e "@_=<>;@_[$XML, $SGML]=@_[$SGML, $XML];print @_" \
    ${CATALOG} > ${CATALOG}.rpmtmp
  mv -f ${CATALOG}.rpmtmp ${CATALOG}
fi

##
## XML catalog
##

CAT_DIR=/usr/share/sgml/docbook/
CATALOG=/usr/share/sgml/docbook/xmlcatalog

if [ -w $CATALOG ]
then
  # DocBook XML V4.1.2
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.1.2-%{version}-%{release}" $CATALOG

  # DocBook XML V4.2
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.2-%{version}-%{release}" $CATALOG

  # DocBook XML V4.3
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-box.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-num.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.3-%{version}-%{release}" $CATALOG

  # DocBook XML V4.4
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isopub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isobox.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isonum.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isodia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isogrk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isocyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isotech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isolat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isolat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isoamsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}/ent/isocyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.4-%{version}-%{release}" $CATALOG

  # DocBook XML V4.5
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isopub.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbpoolx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isobox.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/docbookx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk3.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsn.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isonum.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbcentx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk4.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbnotnx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isodia.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isogrk2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbgenent.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/dbhierx.mod" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsa.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamso.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isocyr1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isotech.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsc.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/soextblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/calstblx.dtd" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isolat1.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsb.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isolat2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isoamsr.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}/ent/isocyr2.ent" $CATALOG
  /usr/bin/xmlcatalog --noout --del \
    "${CAT_DIR}xml-dtd-4.5-%{version}-%{release}" $CATALOG
fi

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

