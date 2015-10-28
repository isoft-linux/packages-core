Name:		libva-intel-driver
Version:	1.6.1
Release:	2
Summary:	VA driver for Intel G45 & HD Graphics family
License:	MIT
URL:		http://freedesktop.org/wiki/Software/vaapi
Source0:	http://www.freedesktop.org/software/vaapi/releases/libva-intel-driver/%{name}-%{version}.tar.bz2
BuildRequires:	libva-devel

%description
VA driver for Intel G45 & HD Graphics family
%prep
%setup -q -n %{name}-%{version}

%build
%configure --enable-drm --enable-wayland --enable-x11 
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -regex ".*\.la$" | xargs rm -f --


%files
%{_libdir}/dri/*.so

%changelog
* Fri Oct 23 2015 cjacker - 1.6.1-2
- Rebuild for new 4.0 release

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- update to 1.6.1

* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

