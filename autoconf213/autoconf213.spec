Summary:    A GNU tool for automatically configuring source code
Name:       autoconf213
Version:    2.13
Release:    36%{?dist}
License:    GPLv2+
URL:        http://www.gnu.org/software/autoconf/
Source:     ftp://prep.ai.mit.edu/pub/gnu/autoconf/autoconf-%{version}.tar.gz
Patch0:     autoconf-2.12-race.patch
Patch1:     autoconf-2.13-mawk.patch
Patch2:     autoconf-2.13-notmp.patch
Patch3:     autoconf-2.13-c++exit.patch
Patch4:     autoconf-2.13-headers.patch
Patch6:     autoconf-2.13-exit.patch
Patch7:     autoconf-2.13-wait3test.patch
Patch8:     autoconf-2.13-make-defs-62361.patch
Patch9:     autoconf-2.13-versioning.patch
Patch10:    autoconf213-destdir.patch
Patch11:    autoconf213-info.patch
Patch12:    autoconf213-testsuite.patch
Requires:   gawk, m4 >= 1.1, coreutils
Buildrequires:   texinfo, m4 >= 1.1, perl, gawk, dejagnu, flex
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to specify
various configuration options.

You should install Autoconf if you are developing software and you
would like to use it to create shell scripts that will configure your
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not their
use.

%prep
%setup -q -n autoconf-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
mv autoconf.texi autoconf213.texi
rm -f autoconf.info

%build
%configure --program-suffix=-%{version}
make

%install
rm -rf ${RPM_BUILD_ROOT}
#makeinstall
make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}/%{_bindir}/autoscan-%{version}
# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -rf ${RPM_BUILD_ROOT}%{_infodir}

%check
#make check


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/autoconf-%{version}/
%doc AUTHORS COPYING NEWS README TODO

%changelog
* Fri Oct 23 2015 cjacker - 2.13-36
- Rebuild for new 4.0 release

