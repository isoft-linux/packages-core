Name:		man-pages
Version:    4.00	
Release:	1
Summary:	Linux man pages

Group:		Core/Runtime/Data
License:	GPL
URL:		http://www.kernel.org/doc/man-pages/
Source0:	https://www.kernel.org/pub/linux/docs/man-pages/man-pages-%{version}.tar.xz
Source1:    https://www.kernel.org/pub/linux/docs/man-pages/man-pages-posix/man-pages-posix-2013-a.tar.xz

BuildRequires: sed, coreutils	

%description
A large collection of man pages (documentation) from the Linux
Documentation Project (LDP).


%prep
%setup -q -a1

%build
mkdir -p man0
for sect in 0 1 3; do
    sed -i "/^\.so /s/man${sect}p/man$sect/" \
        man-pages-posix-2013-a/man${sect}p/*
    mv man-pages-posix-2013-a/man${sect}p/* \
        man$sect/
done

%install
make prefix=$RPM_BUILD_ROOT/usr install
rm -rf $RPM_BUILD_ROOT/usr/share/man/*/iconv*
rm -rf $RPM_BUILD_ROOT/usr/share/man/man2/*xattr*
rm -rf $RPM_BUILD_ROOT/usr/share/man/*/tzfile.*
rm -rf $RPM_BUILD_ROOT/usr/share/man/*/tzselect.*
rm -rf $RPM_BUILD_ROOT/usr/share/man/*/zdump.*
rm -rf $RPM_BUILD_ROOT/usr/share/man/*/zic.*

rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/yacc.*
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man5/attr.*
%files
%{_datadir}/man


%changelog

