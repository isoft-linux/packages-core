Name:           libva-vdpau-driver
Version:        0.7.4
Release:        13%{?dist}
Summary:        HW video decode support for VDPAU platforms
License:        GPLv2+
URL:            http://cgit.freedesktop.org/vaapi/vdpau-driver
Source0:        http://www.freedesktop.org/software/vaapi/releases/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.7.4-glext-85.patch
Patch1:         %{name}-0.7.4-drop-h264-api.patch
Patch2:         %{name}-0.7.4-fix_type.patch

#BuildRequires: libtool
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  mesa-libGL-devel


%description
VDPAU Backend for Video Acceleration (VA) API.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .fix_type

%build
%configure \
  --disable-silent-rules \
  --enable-glx

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/dri/*.so

%changelog
* Fri Oct 23 2015 cjacker - 0.7.4-13
- Rebuild for new 4.0 release

* Sat Sep 26 2015 Cjacker <cjacker@foxmail.com>
- rebuild with libva-1.6.1

