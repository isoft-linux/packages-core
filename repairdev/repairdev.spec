Name:           repairdev
Version:        0.3
Release:        6
Summary:        fix hardware device for isoft linux

License:        GPL
URL:            http://git.isoft.zhcn.cc/wuxiaotian/repairdev
Source0:        http://pkgs.isoft.zhcn.cc/repo/pkgs/repairdev/%{name}-%{version}.tar.xz/9a40083669ea55f7b828ae1c408a93de/%{name}-%{version}.tar.xz

BuildRequires:  pciutils-devel
Requires:       pciutils-libs

%description
fix hardware device for isoft linux

%prep
%setup -q
cp pci.d/8086-29d2.sh pci.d/8086-2e32.sh
cp pci.d/8086-29d2.sh pci.d/8086-2a42.sh

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

%files
%doc
%{_libdir}/systemd/system/%{name}.service
%{_sysconfdir}/pci.d
%{_bindir}/repairdev

%changelog
* Fri Jan 15 2016 xiaotian.wu@i-soft.com.cn - 0.3-6
- fix intel VGA for hp 2230s.

* Wed Dec 30 2015 xiaotian.wu@i-soft.com.cn - 0.3-5
- fix bug 13171.

* Mon Dec 21 2015 sulit <sulitsrc@gmail.com> - 0.3-4
- remove the mouse invisible patch, and hold it for the time being

* Fri Dec 04 2015 sulit <sulitsrc@gmali.com> - 0.3-3
- add fix intel 8086-0102 the mouse invisible patch

* Wed Nov 04 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 0.3-2
- update to 0.3.

* Tue Nov 03 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 0.2-3
- don't use %{_unitdir} on koji.

* Tue Nov 03 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn> - 0.2-2
- rebuilt

* Mon Nov  2 2015 Wu Xiaotian <xiaotian.wu@i-soft.com.cn>
- init. 
