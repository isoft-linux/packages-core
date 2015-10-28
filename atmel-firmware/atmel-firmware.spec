%define usb_version 0.1

Name:           atmel-firmware
Version:        1.3
Release:        15%{?dist}
Summary:        Firmware for Atmel at76c50x wireless network chips

License:        Redistributable, no modification permitted
URL:            http://at76c503a.berlios.de/
Source0:        http://www.thekelleys.org.uk/atmel/atmel-firmware-%{version}.tar.gz
Source1:        http://download.berlios.de/at76c503a/at76_usb-firmware-%{usb_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
    
Obsoletes:      at76_usb-firmware < %{usb_version}
Provides:       at76_usb-firmware = %{usb_version}

%description
The drivers for Atmel at76c50x wireless network chips in the Linux 2.6.x kernel 
but do not include the firmware.
This firmware needs to be loaded by the host on most cards using these chips.


%prep
%setup -q 
%setup -q -D -T -a 1 
install -pm 0644 at76_usb-firmware-%{usb_version}/COPYRIGHT COPYRIGHT-usb
install -pm 0644 at76_usb-firmware-%{usb_version}/README README-usb
for i in COPYING README COPYRIGHT-usb README-usb; do
install -pm 0644 ${i} ${i}.%{name}
rm  ${i}
ln -sf /lib/firmware/${i}.%{name} ${i}
done

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/lib/firmware

install -pm 0644 images/*.bin $RPM_BUILD_ROOT/lib/firmware
#install -m 0644 images.usb/* $RPM_BUILD_ROOT/lib/firmware
install -pm 0644 at76_usb-firmware-%{usb_version}/*.bin $RPM_BUILD_ROOT/lib/firmware
install -pm 0644 *.%{name} $RPM_BUILD_ROOT/lib/firmware

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README COPYRIGHT-usb README-usb VERSION
/lib/firmware/*


%changelog
* Fri Oct 23 2015 cjacker - 1.3-15
- Rebuild for new 4.0 release

