%define osname isoft 
%define osid   isoft 
%define builtin_release_version 4.0 
%define builtin_release_name Nvwa 

%define real_release_version %{?release_version}%{!?release_version:%{builtin_release_version}}
%define real_release_name %{?release_name}%{!?release_name:%{builtin_release_name}}
Summary: iSoft Enterprise Desktop release file
Name: os-release
Version: %{real_release_version}
release: 1.0
License: GPL
Group: Core/Runtime/Data

#Fake a lsb provides for some comercial binary software.
Provides: lsb > 4.0
%description
iSoft Enterprise Desktop release file

%prep
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/etc
cat > $RPM_BUILD_ROOT/usr/lib/%{name} <<-EOF
NAME=%{osname}
VERSION="%{builtin_release_version} (%{builtin_release_name})"
ID=%{osid}
VERSION_ID=%{builtin_release_version}
PRETTY_NAME="%{osname} %{builtin_release_version} (%{builtin_release_name})"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:%{osid}:%{osid}:%{builtin_release_version}"
EOF

pushd $RPM_BUILD_ROOT/etc
ln -sf /usr/lib/os-release .
popd

echo "%{osname} release %{builtin_release_version} (%{real_release_name})" > $RPM_BUILD_ROOT/etc/system-release
echo "%{osname} release %{builtin_release_version} (%{real_release_name})" >$RPM_BUILD_ROOT/etc/issue 
echo "%{osname} release %{builtin_release_version} (%{real_release_name})" >$RPM_BUILD_ROOT/etc/issue.net
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
* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- update for iSoft Enterprise Desktop 4.0

* Tue Dec 24 2013 Cjacker <cjacker@gmail.com>
- for pangu
