Name: docbook-style-dsssl
Version: 1.79
Release: 22%{?dist}

Summary: Norman Walsh's modular stylesheets for DocBook

License: DMIT
URL: http://docbook.sourceforge.net/

Requires: docbook-dtds
Requires: openjade
Requires: sgml-common
Requires(post): sgml-common
Requires(preun): sgml-common

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/docbook/docbook-dsssl-%{version}.tar.gz
Source1: %{name}.Makefile


%description
These DSSSL stylesheets allow to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%prep
%setup -q -n docbook-dsssl-%{version}
cp %{SOURCE1} Makefile


%build

%install
DESTDIR=$RPM_BUILD_ROOT
make install BINDIR=$DESTDIR/usr/bin DESTDIR=$DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets-%{version} MANDIR=$DESTDIR%{_mandir}
cd ..
ln -s dsssl-stylesheets-%{version} $DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets

%files
%defattr (-,root,root,-)
%doc BUGS README ChangeLog WhatsNew
/usr/bin/collateindex.pl
%{_mandir}/man1/collateindex.pl.1*
/usr/share/sgml/docbook/dsssl-stylesheets-%{version}
/usr/share/sgml/docbook/dsssl-stylesheets


%post
for centralized in /etc/sgml/*-docbook-*.cat
do
  /usr/bin/install-catalog --add $centralized \
    /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog \
    > /dev/null 2>/dev/null
done


%preun
if [ "$1" = "0" ]; then
  for centralized in /etc/sgml/*-docbook-*.cat
  do
    /usr/bin/install-catalog --remove $centralized /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog > /dev/null 2>/dev/null
  done
fi
exit 0

%changelog
* Fri Oct 23 2015 cjacker - 1.79-22
- Rebuild for new 4.0 release

