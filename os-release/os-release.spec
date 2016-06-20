%define osname iSoft Desktop
%define osid   iSoft 
%define builtin_release_version 4.0 
%define builtin_release_name Nvwa 

%define real_release_version %{?release_version}%{!?release_version:%{builtin_release_version}}


Summary: iSoft Desktop release file
Name: os-release
Version: %{real_release_version}
release: 4.2
License: GPL

#Fake a lsb provides for some comercial binary software.
Provides: lsb > 4.0
%description
iSoft Desktop release file

%prep
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/etc
cat > $RPM_BUILD_ROOT/usr/lib/%{name} <<-EOF
NAME="%{osname}"
VERSION="%{builtin_release_version}"
ID=%{osid}
VERSION_ID=%{builtin_release_version}
PRETTY_NAME="%{osname} %{builtin_release_version}"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:%{osid}:%{osid}:%{builtin_release_version}"
EOF

pushd $RPM_BUILD_ROOT/etc
ln -sf /usr/lib/os-release .
popd

cat > $RPM_BUILD_ROOT/etc/lsb-release <<-EOF
DISTRIB_ID=%{osid}
DISTRIB_RELEASE=%{builtin_release_version}
DISTRIB_CODENAME=%{builtin_release_name}
DISTRIB_DESCRIPTION="%{osname} %{builtin_release_version}"
EOF

echo "%{osname} %{builtin_release_version}" > $RPM_BUILD_ROOT/etc/system-release
echo "%{osname} %{builtin_release_version}" > $RPM_BUILD_ROOT/etc/issue
echo "%{osname} %{builtin_release_version}" > $RPM_BUILD_ROOT/etc/issue.net
echo "Kernel \r on an \m" >>$RPM_BUILD_ROOT/etc/issue
echo "" >>$RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >>$RPM_BUILD_ROOT/etc/issue.net
echo "" >>$RPM_BUILD_ROOT/etc/issue.net


%clean

%files
%defattr(-,root,root)
%attr(0755,root,root) /etc/
/usr/lib/os-release

%changelog
* Mon Jan 04 2016 sulit <sulitsrc@gmail.com> - 4.0-4.2
- remove real_release_name due to design

* Mon Dec 21 2015 Cjacker <cjacker@foxmail.com> - 4.0-3.2
- Rename to iSoft Desktop

* Fri Oct 23 2015 cjacker - 4.0-2.2
- Rebuild for new 4.0 release

* Sun Oct 18 2015 Cjacker <cjacker@foxmail.com>
- add lsb-release

* Mon Oct 12 2015 Cjacker <cjacker@foxmail.com>
- update to change osname from "isoft" to "iSoft Enterprise Desktop"

* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- update for iSoft Enterprise Desktop 4.0

* Tue Dec 24 2013 Cjacker <cjacker@gmail.com>
- for pangu
