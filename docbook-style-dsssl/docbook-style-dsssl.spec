Name: docbook-style-dsssl
Version: 1.79
Release: 5
Group:   CoreDev/Development/Utility/Documentation

Summary: Norman Walsh's modular stylesheets for DocBook

License: Freely redistributable without restriction
URL: http://docbook.sourceforge.net/

%define openjadever 1.3.2
Requires: openjade = %{openjadever}
Requires: docbook-dtds >= 1.0-19
Requires: sgml-common >= 0.5
Requires: openjade = %{openjadever}
Conflicts: docbook-utils < 0.6.9-4

BuildRoot: %{_tmppath}/%{name}-%{version}

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
rm -rf $RPM_BUILD_ROOT
make install BINDIR=$DESTDIR/usr/bin DESTDIR=$DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets-%{version}
cd ..
ln -s dsssl-stylesheets-%{version} $DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root)
%doc BUGS README ChangeLog WhatsNew
/usr/bin/collateindex.pl
/usr/share/sgml/docbook/dsssl-stylesheets-%{version}
/usr/share/sgml/docbook/dsssl-stylesheets


%post
rel=$(echo /etc/sgml/sgml-docbook-3.0-*.cat)
rel=${rel##*-}
rel=${rel%.cat}
for centralized in /etc/sgml/*-docbook-*.cat
do
  /usr/bin/install-catalog --remove $centralized \
    /usr/share/sgml/docbook/dsssl-stylesheets-*/catalog \
    >/dev/null 2>/dev/null
done

for centralized in /etc/sgml/*-docbook-*$rel.cat
do
  /usr/bin/install-catalog --add $centralized \
    /usr/share/sgml/openjade-%{openjadever}/catalog \
    > /dev/null 2>/dev/null
  /usr/bin/install-catalog --add $centralized \
    /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog \
    > /dev/null 2>/dev/null
done


%preun
if [ "$1" = "0" ]; then
  for centralized in /etc/sgml/*-docbook-*.cat
  do   /usr/bin/install-catalog --remove $centralized /usr/share/sgml/openjade-%{openjadever}/catalog > /dev/null 2>/dev/null
    /usr/bin/install-catalog --remove $centralized /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog > /dev/null 2>/dev/null
  done
fi
exit 0

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

