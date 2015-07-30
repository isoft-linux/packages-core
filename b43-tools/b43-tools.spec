%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:		b43-tools
Version:	017
Release:	5%{?dist}
Summary:	Tools for the Broadcom 43xx series WLAN chip
Group:		System Environment/Base
# assembler — GPLv2
# debug — GPLv3
# disassembler — GPLv2
# ssb_sprom — GPLv2+
License:	GPLv2 and GPLv2+ and GPLv3
URL:		http://bues.ch/gitweb?p=b43-tools.git;a=summary
## git clone git://git.bues.ch/b43-tools.git
## cd b43-tools
## git-archive --format=tar --prefix=%{name}-%{version}/ b43-fwcutter-%{version} | xz > ../%{name}-%{version}.tar.xz
Source0:	%{name}-%{version}.tar.xz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	python-devel


%description
Tools for the Broadcom 43xx series WLAN chip.


%prep
%setup -q
install -p -m 0644 assembler/COPYING COPYING.assembler
install -p -m 0644 assembler/README README.assembler
install -p -m 0644 debug/COPYING COPYING.debug
install -p -m 0644 debug/README README.debug
install -p -m 0644 disassembler/COPYING COPYING.disassembler
install -p -m 0644 ssb_sprom/README README.ssb_sprom
install -p -m 0644 ssb_sprom/COPYING COPYING.ssb_sprom


%build
CFLAGS="%{optflags}" make %{?_smp_mflags} -C assembler
CFLAGS="%{optflags}" make %{?_smp_mflags} -C disassembler
CFLAGS="%{optflags}" make %{?_smp_mflags} -C ssb_sprom
cd debug && python install.py build


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 assembler/b43-asm %{buildroot}%{_bindir}
install -p -m 0755 assembler/b43-asm.bin %{buildroot}%{_bindir}
install -p -m 0755 disassembler/b43-dasm %{buildroot}%{_bindir}
install -p -m 0755 disassembler/b43-ivaldump %{buildroot}%{_bindir}
install -p -m 0755 disassembler/brcm80211-fwconv %{buildroot}%{_bindir}
install -p -m 0755 disassembler/brcm80211-ivaldump %{buildroot}%{_bindir}
install -p -m 0755 ssb_sprom/ssb-sprom %{buildroot}%{_bindir}
cd debug && python install.py install --skip-build --root %{buildroot}


%files
%doc README.* COPYING.*
%{_bindir}/b43-asm
%{_bindir}/b43-asm.bin
%{_bindir}/b43-beautifier
%{_bindir}/b43-dasm
%{_bindir}/b43-fwdump
%{_bindir}/b43-ivaldump
%{_bindir}/brcm80211-fwconv
%{_bindir}/brcm80211-ivaldump
%{_bindir}/ssb-sprom
%{python_sitelib}/*


%changelog
