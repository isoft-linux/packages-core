%define opensp_ver 1.5
Summary: A DSSSL implementation.
Name: openjade
Version: 1.3.2
Release: 16
Requires(pre): sgml-common >= 0.5
Requires(pre): docbook-dtds
Source0: http://download.sourceforge.net/openjade/openjade-%{version}.tar.gz
Source1: http://download.sourceforge.net/openjade/OpenSP-%{opensp_ver}.tar.gz
Patch0: openjade-1.3.1-manpage.patch
Patch2: openjade-clang.patch
Patch5: msggen.pl.patch

Patch10: opensp-1.5-gcc34.patch

License: Distributable
Group:  CoreDev/Development/Utility/Documentation
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: /usr
Obsoletes: jade
Provides: jade

BuildRequires: autoconf, automake, gettext-devel

%description
OpenJade is an implementation of the ISO/IEC 10179:1996 standard DSSSL
(Document Style Semantics and Specification Language). OpenJade is
based on James Clark's Jade implementation of DSSSL. OpenJade is a
command-line application and a set of components. The DSSSL engine
inputs an SGML or XML document and can output a variety of formats:
XML, RTF, TeX, MIF (FrameMaker), SGML, or XML.

%package devel
Summary: Files for developing applications that use openjade/OpenSP.
Requires: %{name} = %{version}
Group: CoreDev/Development/Library

%description devel
The header files, static library, libtool library and man pages for
developing applications that use openjade/OpenSP.

%define openjadetop %{_builddir}/%{name}-%{version}
%prep
%setup -q -c -a1

pushd %{openjadetop}/openjade-%{version}
%patch0 -p1 -b .manpage
%patch2 -p1
%patch5 -p1
popd

pushd %{openjadetop}/OpenSP-%{opensp_ver}
%patch10 -p1
popd

%build
export CFLAGS+=" -fpermissive"
export CPPFLAGS+=" -fpermissive"
export CXXFLAGS+=" -fpermissive"
pushd %{openjadetop}/OpenSP-%{opensp_ver}
aclocal
libtoolize --copy --force
automake --add-missing --copy
autoconf --force
%configure --enable-http --datadir=/usr/share/sgml/%{name}-%{version} \
 --enable-default-catalog=/etc/sgml/catalog \
 --enable-default-search-path=/usr/share/sgml
make %{?_smp_mflags}
# This is needed because openjade has an awful hack in its own config.h.
cp config.h include
# This is to catch #include <OpenSP/...>
ln -s . include/OpenSP
popd

pushd %{openjadetop}/openjade-%{version}
#cp config/configure.in .
#libtoolize --copy --force
%configure --enable-http --datadir=/usr/share/sgml/%{name}-%{version} \
 --enable-spincludedir=%{openjadetop}/OpenSP-%{opensp_ver}/include \
 --enable-splibdir=%{openjadetop}/OpenSP-%{opensp_ver}/lib \
 --enable-default-catalog=/etc/sgml/catalog \
 --enable-default-search-path=/usr/share/sgml
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

pushd %{openjadetop}/OpenSP-%{opensp_ver}
%makeinstall datadir=$RPM_BUILD_ROOT/usr/share/sgml/%{name}-%{version}
make install-man mandir=$RPM_BUILD_ROOT/%{_mandir}
popd

pushd %{openjadetop}/openjade-%{version}
%makeinstall datadir=$RPM_BUILD_ROOT/usr/share/sgml/%{name}-%{version}
make install-man mandir=$RPM_BUILD_ROOT/%{_mandir}
popd

# Fix up libtool libraries
find $RPM_BUILD_ROOT -name '*.la' | \
  xargs perl -p -i -e "s|-L$RPM_BUILD_DIR[\w/.-]*||g"

# oMy, othis ois osilly.
ln -s openjade $RPM_BUILD_ROOT/%{prefix}/bin/jade
echo ".so man1/openjade.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/jade.1
for file in nsgmls sgmlnorm spam spent sx ; do
   ln -s o$file $RPM_BUILD_ROOT/%{prefix}/bin/$file
   echo ".so man1/o${file}.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/${file}.1
done

mv $RPM_BUILD_ROOT/%{prefix}/bin/sx $RPM_BUILD_ROOT/%{prefix}/bin/sgml2xml
mv $RPM_BUILD_ROOT/%{_mandir}/man1/{sx,sgml2xml}.1

# install jade/jade $RPM_BUILD_ROOT/%{prefix}/bin/jade 
cp %{openjadetop}/openjade-%{version}/dsssl/catalog $RPM_BUILD_ROOT/%{prefix}/share/sgml/%{name}-%{version}/
cp %{openjadetop}/openjade-%{version}/dsssl/dsssl.dtd \
  %{openjadetop}/openjade-%{version}/dsssl/style-sheet.dtd \
  %{openjadetop}/openjade-%{version}/dsssl/fot.dtd \
  $RPM_BUILD_ROOT/%{prefix}/share/sgml/%{name}-%{version}

rm -rf $RPM_BUILD_ROOT/usr/doc/OpenSP
rm -rf $RPM_BUILD_ROOT/%{prefix}/share/sgml/%{name}-%{version}/doc
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rpmclean
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
 
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{prefix}/share/sgml
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

