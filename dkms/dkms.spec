Summary:        Dynamic Kernel Module Support Framework
Name:           dkms
Version:        2.3
Release:        1
License:        GPLv2+
BuildArch:      noarch
URL:            http://linux.dell.com/dkms
Source0:        https://github.com/dell/%{name}/archive/%{version}.tar.gz
Requires:       coreutils
Requires:       cpio
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       gcc
Requires:       grep
Requires:       gzip
Requires:       kernel-devel
Requires:       kmod
Requires:       sed
Requires:       tar
Requires:       which

BuildRequires:          systemd
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description
This package contains the framework for the Dynamic Kernel Module Support (DKMS)
method for installing module RPMS as originally developed by Dell.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}

make install-redhat-systemd DESTDIR=%{buildroot} \
    LIBDIR=%{buildroot}%{_prefix}/lib/%{name} \
    SYSTEMD=%{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}

%post
%systemd_post %{name}_autoinstaller.service

%preun
%systemd_preun %{name}_autoinstaller.service

%postun
%systemd_postun %{name}_autoinstaller.service

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc sample.spec sample.conf AUTHORS README.dkms
%{_unitdir}/%{name}.service
%{_prefix}/lib/%{name}
%{_mandir}/man8/dkms.8*
%{_sbindir}/%{name}
%{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}

%changelog
* Wed Dec 07 2016 sulit - 2.3-1
- upgrade dkms to 2.3

* Fri Nov 13 2015 Cjacker <cjacker@foxmail.com> - 2.2.0.3-2
- Initial build

