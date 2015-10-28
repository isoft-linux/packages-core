Name:		polkit-pkla-compat
Version:	0.1
Release:	7%{?dist}
Summary:	Rules for polkit to add compatibility with pklocalauthority
# GPLv2-licensed ltmain.sh and Apache-licensed mocklibc are not shipped in
# the binary package.
License:	LGPLv2+
URL:		https://fedorahosted.org/polkit-pkla-compat/
Source0:	https://fedorahosted.org/releases/p/o/polkit-pkla-compat/polkit-pkla-compat-%{version}.tar.xz

BuildRequires:	docbook-style-xsl, libxslt, glib2-devel, polkit-devel
# To ensure the polkitd group already exists when this is installed
Requires(pre): polkit

%description
A polkit JavaScript rule and associated helpers that mostly provide
compatibility with the .pkla file format supported in polkit <= 0.105 for users
of later polkit releases.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
%make_install INSTALL='install -p'

%check
make check

%files
%doc AUTHORS COPYING NEWS README
%dir %attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/localauthority
%dir %{_sysconfdir}/polkit-1/localauthority/*.d
%dir %{_sysconfdir}/polkit-1/localauthority.conf.d
%config(noreplace) %{_sysconfdir}/polkit-1/rules.d/49-polkit-pkla-compat.rules
%{_bindir}/pkla-admin-identities
%{_bindir}/pkla-check-authorization
%{_mandir}/man8/pkla-admin-identities.8*
%{_mandir}/man8/pkla-check-authorization.8*
%{_mandir}/man8/pklocalauthority.8*
%dir %attr(0750,root,polkitd) %{_localstatedir}/lib/polkit-1
%dir %{_localstatedir}/lib/polkit-1/localauthority
%dir %{_localstatedir}/lib/polkit-1/localauthority/*.d

%changelog
* Fri Oct 23 2015 cjacker - 0.1-7
- Rebuild for new 4.0 release

