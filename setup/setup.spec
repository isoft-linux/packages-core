Summary: A set of system configuration and setup files
Name: setup
Version: 2.9.8
Release: 3%{?dist}
License: Public Domain
URL: https://fedorahosted.org/setup/
Source0: https://fedorahosted.org/releases/s/e/%{name}/%{name}-%{version}.tar.bz2
Patch0: setup-add-default-user-group.patch
Patch1: setup-remove-tcsh.patch

BuildArch: noarch
BuildRequires: bash perl

%description
The setup package contains a set of important system configuration and
setup files, such as passwd, group, and profile.

%prep
%setup -q
./shadowconvert.sh
%patch0 -p1
%patch1 -p1

%build

%check
# Run any sanity checks.
make check

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
cp -ar * %{buildroot}/etc
rm -f %{buildroot}/etc/uidgid
rm -f %{buildroot}/etc/COPYING
mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/lastlog
touch %{buildroot}/etc/environment
chmod 0644 %{buildroot}/etc/environment
chmod 0400 %{buildroot}/etc/{shadow,gshadow}
chmod 0644 %{buildroot}/var/log/lastlog
touch %{buildroot}/etc/fstab

# remove unpackaged files from the buildroot
rm -f %{buildroot}/etc/Makefile
rm -f %{buildroot}/etc/serviceslint
rm -f %{buildroot}/etc/uidgidlint
rm -f %{buildroot}/etc/shadowconvert.sh
rm -f %{buildroot}/etc/setup.spec

%clean
rm -rf %{buildroot}

#throw away useless and dangerous update stuff until rpm will be able to
#handle it ( http://rpm.org/ticket/6 )
%post -p <lua>
for i, name in ipairs({"passwd", "shadow", "group", "gshadow"}) do
     os.remove("/etc/"..name..".rpmnew")
end
if posix.access("/usr/bin/newaliases", "x") then
  os.execute("/usr/bin/newaliases >/dev/null")
end

%files
%defattr(-,root,root,-)
%doc uidgid COPYING
%verify(not md5 size mtime) %config(noreplace) /etc/passwd
%verify(not md5 size mtime) %config(noreplace) /etc/group
%verify(not md5 size mtime) %attr(0400,root,root) %config(noreplace,missingok) /etc/shadow
%verify(not md5 size mtime) %attr(0400,root,root) %config(noreplace,missingok) /etc/gshadow
%config(noreplace) /etc/services
%verify(not md5 size mtime) %config(noreplace) /etc/exports
%config(noreplace) /etc/aliases
%config(noreplace) /etc/environment
%config(noreplace) /etc/filesystems
%config(noreplace) /etc/host.conf
%verify(not md5 size mtime) %config(noreplace) /etc/hosts
%config(noreplace) /etc/hosts.allow
%config(noreplace) /etc/hosts.deny
%verify(not md5 size mtime) %config(noreplace) /etc/motd
%config(noreplace) /etc/printcap
%verify(not md5 size mtime) %config(noreplace) /etc/inputrc
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/profile
%config(noreplace) /etc/protocols
%config(noreplace) /etc/csh.login
%config(noreplace) /etc/csh.cshrc
%dir /etc/profile.d
%config(noreplace) %verify(not md5 size mtime) /etc/shells
%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/fstab

%changelog
* Fri Oct 23 2015 cjacker - 2.9.8-3
- Rebuild for new 4.0 release

