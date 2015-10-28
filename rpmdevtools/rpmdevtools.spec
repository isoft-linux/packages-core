%global spectool_version 1.0.10

Name:           rpmdevtools
Version:        8.6
Release:        2%{?dist}
Summary:        RPM Development Tools

# rpmdev-setuptree is GPLv2, everything else GPLv2+
License:        GPLv2+ and GPLv2
URL:            https://fedorahosted.org/rpmdevtools/
Source0:        https://fedorahosted.org/released/rpmdevtools/%{name}-%{version}.tar.xz

BuildArch:      noarch
# help2man, pod2man, *python for creating man pages
BuildRequires:  help2man
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  python >= 2.6
BuildRequires:  bash-completion
#%if 0%{?fedora}
## xemacs-common >= 21.5.29-8 for macros.xemacs
#BuildRequires:  xemacs-common >= 21.5.29-8
#%endif
Provides:       spectool = %{spectool_version}
Requires:       curl
Requires:       diffutils
Requires:       fakeroot
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       grep
Requires:       python >= 2.4
Requires:       rpm-build >= 4.4.2.3
#Requires:       rpm-python
Requires:       sed
#Requires:       emacs-filesystem

%description
This package contains scripts and (X)Emacs support files to aid in
development of RPM packages.
rpmdev-setuptree    Create RPM build tree within user's home directory
rpmdev-diff         Diff contents of two archives
rpmdev-newspec      Creates new .spec from template
rpmdev-rmdevelrpms  Find (and optionally remove) "development" RPMs
rpmdev-checksig     Check package signatures using alternate RPM keyring
rpminfo             Print information about executables and libraries
rpmdev-md5/sha*     Display checksums of all files in an archive file
rpmdev-vercmp       RPM version comparison checker
spectool            Expand and download sources and patches in specfiles
rpmdev-wipetree     Erase all files within dirs created by rpmdev-setuptree
rpmdev-extract      Extract various archives, "tar xvf" style
rpmdev-bumpspec     Bump revision in specfile
...and many more.


%prep
%setup -q


%build
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

echo %%{_datadir}/bash-completion > %{name}.files
[ -d $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d ] && \
echo %%{_sysconfdir}/bash_completion.d > %{name}.files


%files -f %{name}.files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS
%config(noreplace) %{_sysconfdir}/rpmdevtools/
%{_datadir}/rpmdevtools/
%{_bindir}/*
%{_mandir}/man[18]/*.[18]*


%changelog
* Fri Oct 23 2015 cjacker - 8.6-2
- Rebuild for new 4.0 release

* Sun May 10 2015 Ville Skyttä <ville.skytta@iki.fi> - 8.6-1
- Update to 8.6

