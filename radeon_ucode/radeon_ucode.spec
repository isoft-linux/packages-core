#This package as a supplementary to linux-firmware.
#Some new firmware that still not in linux-firmware, for example, tonga.

Name:		radeon_ucode
Version:	20150907
Release:	2
Summary:	IRQ microcode for r6xx/r7xx/Evergreen/N.Islands/S.Islands and other new Radeon GPUs and APUs

License:	Redistributable	
URL:		https://secure.freedesktop.org/~agd5f/radeon_ucode/
#wget -c -r -np -k -L -p https://secure.freedesktop.org/~agd5f/radeon_ucode/
Source0:	radeon_ucode.tar.gz	
#firmware already in linux-firmware
Source1: 	firmware-in-linux-firmware
BuildArch: noarch

%description
%{summary}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n radeon_ucode

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/firmware/radeon/
mkdir -p %{buildroot}%{_libdir}/firmware/amdgpu/

cp secure.freedesktop.org/~agd5f/radeon_ucode/*.bin %{buildroot}%{_libdir}/firmware/radeon/
cp secure.freedesktop.org/~agd5f/radeon_ucode/*/*.bin %{buildroot}%{_libdir}/firmware/radeon/


pushd %{buildroot}%{_libdir}/firmware/radeon
for i in `cat %{SOURCE1}`
do
	rm -rf $i
done

#for amdgpu
rm -rf topaz_*
rm -rf tonga_*
rm -rf carrizo_*
rm -rf fiji_*
popd

%files
%{_libdir}/firmware/radeon/*.bin
#%{_libdir}/firmware/amdgpu/*.bin

%changelog
* Fri Oct 23 2015 cjacker - 20150907-2
- Rebuild for new 4.0 release

* Thu Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update, add fiji firmware
* Sun Jul 26 2015 Cjacker <cjacker@foxmail.com>
- add amdgpu firmware.
