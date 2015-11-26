Name: autoconf-archive
Version: 2015.09.25
Release: 2
Summary: A collection of more than 500 macros for GNU Autoconf 

License:        GPLv3+ with exceptions

URL: http://www.gnu.org/software/autoconf-archive/
Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildArch: noarch

Requires: autoconf
BuildRequires: info

%description
The GNU Autoconf Archive is a collection of more than 450 macros for
GNU Autoconf that have been contributed as free software by friendly
supporters of the cause from all over the Internet.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_infodir}
# document files are installed another location
rm -frv %{buildroot}%{_datadir}/%{name}

%files
%doc AUTHORS NEWS README TODO
%license COPYING*
%{_datadir}/aclocal/*.m4

%changelog
* Thu Nov 26 2015 Cjacker <cjacker@foxmail.com> - 2015.09.25-2
- Initial build

