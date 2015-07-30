Summary: A GNU tool which simplifies the build process for users
Name: make
Epoch: 1
Version: 4.0 
Release: 6
License: GPL
Group:  CoreDev/Development/Utility
URL: http://www.gnu.org/software/make/
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
%setup -q
%build
%configure --without-guile
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake

rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -rf $RPM_BUILD_ROOT%{_includedir}

%find_lang make

rpmclean

%check
echo ============TESTING===============
/usr/bin/env LANG=C make check ||:
echo ============END TESTING===========

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f make.lang 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*

%changelog
* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
