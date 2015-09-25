Name: isoft-update-client
Version: 0.1.0
Release: 1%{?dist}
Summary: iSOFT Update Client

License: GPLv2 or GPLv3
URL: http://git.isoft.zhcn.cc/zhaixiang/isoft-update-client
Source0: %{name}-%{version}.tar.bz2

BuildRequires: extra-cmake-modules
BuildRequires: kf5-rpm-macros
BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: dbus-glib-devel
BuildRequires: systemd-units
BuildRequires: systemd-devel
BuildRequires: libcurl-devel
BuildRequires: libxml2-devel
BuildRequires: xz-devel
BuildRequires: librpm-devel
BuildRequires: popt-devel
BuildRequires: libtar-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtquickcontrols-devel
BuildRequires: kf5-kdelibs4support-devel
BuildRequires: kf5-plasma-devel
BuildRequires: kf5-ki18n-devel

Requires: kf5-filesystem
Requires: systemd 

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
iSOFT Update Client.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang plasma_applet_org.kde.plasma.isoftupdate

%post
%systemd_post isoft-update-daemon.service

%preun
%systemd_preun isoft-update-daemon.service

%postun
%systemd_postun isoft-update-daemon.service


%files -f plasma_applet_org.kde.plasma.isoftupdate.lang
%doc README.md
%{_sysconfdir}/isoft-update.conf
%{_sysconfdir}/dbus-1/system.d/org.isoftlinux.Update.conf
%{_datadir}/dbus-1/interfaces/org.isoftlinux.Update.xml
%{_datadir}/dbus-1/system-services/org.isoftlinux.Update.service
%{_unitdir}/isoft-update-daemon.service
%{_bindir}/isoft-update-daemon
%{_bindir}/isoft-update-console
%{_bindir}/isoft-update-server-tool
# kcm
%{_kf5_qtplugindir}/kcm_isoftupdate.so
%{_kf5_datadir}/kservices5/kcm_isoftupdate.desktop
%{_kf5_qtplugindir}/kcm_isoftupdate_viewer.so
%{_kf5_datadir}/kservices5/kcm_isoftupdate_viewer.desktop
# plasmoid
%{_qt5_prefix}/qml/org/kde/plasma/isoftupdate/libplasma_applet_isoftupdate.so
%{_qt5_prefix}/qml/org/kde/plasma/isoftupdate/qmldir
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.isoftupdate/
%{_datadir}/plasma/plasmoids/org.kde.plasma.isoftupdate/contents
%{_datadir}/plasma/plasmoids/org.kde.plasma.isoftupdate/metadata.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.plasma.isoftupdate.desktop


%changelog

