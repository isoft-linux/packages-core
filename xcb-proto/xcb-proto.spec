Name: xcb-proto 
Version: 1.11
Release: 6.git 
Summary: A C binding to the X11 protocol

License: MIT
URL: http://xcb.freedesktop.org/

#Source0: http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
#git clone git://anongit.freedesktop.org/git/xcb/proto
Source0: xcb-proto-e500bd8.tar.gz

BuildRequires: autoconf automake libtool pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-filesystem
Requires: xorg-x11-filesystem

BuildArch: noarch
%description
xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
generate the majority of its code and API. We provide them separately
from libxcb to allow reuse by other projects, such as additional
language bindings, protocol dissectors, or documentation generators.

%package python 
Summary: python files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: python 

%description python 
xcb-proto also contains language-independent Python
libraries that are used to parse an XML description and create objects
used by Python code generators in individual language bindings. 

%prep
%setup -q -n xcb-proto 

%build
./autogen.sh
%configure --disable-static --docdir=%{_datadir}/doc/%{name}-%{version}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_datadir}/xcb
%{_libdir}/python?.?/site-packages/xcbgen


%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 1.11-6.git
- Update to git e500bd8

* Fri Oct 23 2015 cjacker - 1.11-5.git
- Rebuild for new 4.0 release

* Mon Oct 19 2015 Cjacker <cjacker@foxmail.com>
- rebuild
