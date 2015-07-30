Summary: Terminal emulator for the X Window System
Name: xterm
Version: 318
Release: 2 
URL: http://dickey.his.com/xterm
License: MIT
Group: User Interface/X
BuildRequires: pkgconfig ncurses-devel
BuildRequires: libXft-devel libXaw-devel libXext-devel

Source0: ftp://invisible-island.net/xterm/%{name}-%{version}.tgz
Source1: ftp://invisible-island.net/xterm/16colors.txt

%define x11_app_defaults_dir %(pkg-config --variable appdefaultdir xt)

%description
The xterm program is a terminal emulator for the X Window System. It
provides DEC VT102 and Tektronix 4014 compatible terminals for
programs that can't use the window system directly.

%prep
%setup -q -n xterm-%{version}

%build
%configure \
	--enable-256-color \
	--enable-exec-xterm \
	--enable-luit \
	--enable-warnings \
	--enable-wide-chars \
	--with-app-defaults=%{x11_app_defaults_dir} \
	--with-utempter \
	--with-tty-group=tty \
	--disable-full-tgetent

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

cp -fp %{SOURCE1} 16colors.txt

rpmclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/xterm
%{_bindir}/koi8rxterm
%{_bindir}/resize
%{_bindir}/uxterm
%{_mandir}/man1/koi8rxterm.1*
%{_mandir}/man1/resize.1*
%{_mandir}/man1/uxterm.1*
%{_mandir}/man1/xterm.1*
%{_datadir}/pixmaps/xterm*.xpm
%{x11_app_defaults_dir}/KOI8RXTerm
%{x11_app_defaults_dir}/UXTerm
%{x11_app_defaults_dir}/XTerm
%{x11_app_defaults_dir}/XTerm-color
%{x11_app_defaults_dir}/KOI8RXTerm-color
%{x11_app_defaults_dir}/UXTerm-color
%{_datadir}/pixmaps/*

%changelog
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

