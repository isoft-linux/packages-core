%ifos linux
%define _bindir /bin
%endif

Summary: A GNU stream text editor.
Name: sed
Version: 4.2.2
Release: 1.2
License: GPL
Group: Core/Runtime/Utility
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.bz2

Prefix: %{_prefix}

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q

%build
%configure
make %{_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall
rm -rf ${RPM_BUILD_ROOT}/%{_infodir}

%find_lang sed
rpmclean
%check
make check


%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f sed.lang
%defattr(-,root,root)
%{_bindir}/sed
%{_mandir}/man*/*
%changelog
