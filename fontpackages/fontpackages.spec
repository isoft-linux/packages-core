#we only need macros from this package to support src.rpm directly come from fedora project.

%global spectemplatedir %{_sysconfdir}/rpmdevtools/
%global ftcgtemplatedir %{_datadir}/fontconfig/templates/
%global rpmmacrodir     %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d/)

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Name:    fontpackages
Version: 1.44
Release: 13%{?dist}
Summary: Common directory and macro definitions used by font packages

Group:     Development/System
# Mostly means the scriptlets inserted via this package do not change the
# license of the packages they're inserted in
License:   LGPLv3+
URL:       http://fedoraproject.org/wiki/fontpackages
Source0:   http://fedorahosted.org/releases/f/o/%{name}/%{name}-%{version}.tar.xz

BuildArch: noarch


%description
This package contains the basic directory layout, spec templates, rpm macros
and other materials used to create font packages.


%package filesystem
Summary: Directories used by font packages
License: Public Domain

%description filesystem
This package contains the basic directory layout used by font packages,
including the correct permissions for the directories.


%package devel
Summary: Templates and macros used to create font packages

Requires: %{name}-filesystem = %{version}-%{release}
Requires: fontconfig

%description devel
This package contains spec templates, rpm macros and other materials used to
create font packages.


%package tools
Summary: Tools used to check fonts and font packages

Requires: fontconfig, fontforge
Requires: curl, make
#do not requires it.
#Requires: rpmlint

%description tools
This package contains tools used to check fonts and font packages.


%prep
%setup -q
sed -i 's|/usr/bin/fedoradev-pkgowners|""|g' bin/repo-font-audit

# Drop obosolete %defattr (#1047031)
sed -i '/^%%defattr/d' rpm/macros.fonts

%build
sed -i "s|^DATADIR\([[:space:]]*\)\?=\(.*\)$|DATADIR=%{_datadir}/%{name}|g" \
  bin/repo-font-audit bin/compare-repo-font-audit

%install
# Pull macros out of macros.fonts and emulate them during install
for dir in fontbasedir        fontconfig_masterdir \
           fontconfig_confdir fontconfig_templatedir ; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" \
    rpm/macros.fonts | %{__awk} '{ print $2 }'))
done

install -m 0755 -d %{buildroot}${_fontbasedir} \
                   %{buildroot}${_fontconfig_masterdir} \
                   %{buildroot}${_fontconfig_confdir} \
                   %{buildroot}${_fontconfig_templatedir} \
                   %{buildroot}%{spectemplatedir} \
                   %{buildroot}%{rpmmacrodir} \
                   %{buildroot}%{_datadir}/fontconfig/templates \
                   %{buildroot}/%_datadir/%{name} \
                   %{buildroot}%{_bindir}
install -m 0644 -p spec-templates/*.spec       %{buildroot}%{spectemplatedir}
install -m 0644 -p fontconfig-templates/*      %{buildroot}%{ftcgtemplatedir}
install -m 0644 -p rpm/macros*                 %{buildroot}%{rpmmacrodir}
install -m 0644 -p private/repo-font-audit.mk  %{buildroot}/%{_datadir}/%{name}
install -m 0755 -p private/core-fonts-report \
                   private/font-links-report \
                   private/fonts-report \
                   private/process-fc-query \
                   private/test-info           %{buildroot}/%{_datadir}/%{name}
install -m 0755 -p bin/*                       %{buildroot}%{_bindir}

cat <<EOF > %{name}-%{version}.files
%dir ${_fontbasedir}
%dir ${_fontconfig_masterdir}
%dir ${_fontconfig_confdir}
%dir ${_fontconfig_templatedir}
EOF


#NOTE:
#we do not ship these files on iSoft linux
rm -rf %{buildroot}%{_bindir}/compare-repo-font-audit
rm -rf %{buildroot}%{_bindir}/repo-font-audit
rm -rf %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_bindir}/*

%changelog



%files filesystem -f %{name}-%{version}.files
%dir %{_datadir}/fontconfig

%files devel
%license license.txt
%doc readme.txt
%config(noreplace) %{spectemplatedir}/*.spec
%{rpmmacrodir}/macros*
%dir %{ftcgtemplatedir}
%{ftcgtemplatedir}/*conf
%{ftcgtemplatedir}/*txt

#%files tools
#%license license.txt
#%doc readme.txt
#%dir %{_datadir}/%{name}
#%{_datadir}/%{name}/repo-font-audit.mk
#%{_datadir}/%{name}/core-fonts-report
#%{_datadir}/%{name}/font-links-report
#%{_datadir}/%{name}/fonts-report
#%{_datadir}/%{name}/process-fc-query
#%{_datadir}/%{name}/test-info
#%{_bindir}/*

%changelog
