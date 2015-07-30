Name:	isoft-get-sources
Version:	1.0
Release:	1
Summary: 	isoft get source from scms
Group:	isoft-tools
License:	GPLv3
URL:		http://git.isoft.zhcn.cc/wangguofeng/%{name}
Source0:	http://git.isoft.zhcn.cc/wangguofeng/%{name}-%{version}-%{release}.tar.gz


%description
isoft get soure from scms


%prep
%setup -q


%build


%install
mkdir -p %{buildroot}/usr/bin
make install DEST=%{buildroot}


%files
%defattr(-,root,root)
#%{_bindir}/%{name}
%{_bindir}/isoft_get_sources


%changelog
* Wed Jul 29 2015 sulit <sulitsrc@163.com> - 1.0
- init isoft-get-sources
