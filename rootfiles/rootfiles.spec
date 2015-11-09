Summary: The basic required files for the root user's directory.
Name: rootfiles
Version: 8.1
Release: 10.1 
License: Public Domain
 
Source0: dot-bashrc
Source1: dot-bash_profile
Source2: dot-bash_logout
Source3: dot-tcshrc
Source4: dot-cshrc
Source5: dot-vimrc
Source6: dot-Xresources
Source7: dot-zshrc
BuildRoot: %{_tmppath}/%{name}%{name}-root
BuildArch: noarch

%description
The rootfiles package contains basic required files that are placed
in the root user's account.  These files are basically the same
as those in /etc/skel, which are placed in regular
users' home directories.

%prep

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/root

for file in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7}; do 
  f=`basename $file`
  install -m 644 $file $RPM_BUILD_ROOT/root/${f/dot-/.}
done
mkdir -p $RPM_BUILD_ROOT/etc/skel
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/skel/.Xresources
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/skel/.zshrc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) /root/.[A-Za-z]*
%config(noreplace) /etc/skel/.Xresources
%config(noreplace) /etc/skel/.zshrc

%changelog
* Mon Nov 09 2015 Cjacker <cjacker@foxmail.com> - 8.1-10.1
- add dot-zshrc

* Fri Oct 23 2015 cjacker - 8.1-9.1
- Rebuild for new 4.0 release

