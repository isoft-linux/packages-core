Summary: A perfect hash function generator.
Name: gperf
Version: 3.0.4
Release: 2
License: GPL
Source: ftp://ftp.gnu.org/pub/gnu/gperf/gperf-%{version}.tar.gz
URL: http://www.gnu.org/software/gperf/

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# remove the stuff from the buildroot
rm -rf $RPM_BUILD_ROOT{%{_mandir}/{dvi,html},%{_datadir}/doc}
rm -rf $RPM_BUILD_ROOT%{_infodir}


%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/gperf.1*

%changelog
* Fri Oct 23 2015 cjacker - 3.0.4-2
- Rebuild for new 4.0 release

* Mon Jul 30 2007 Cjacker <cjacker@gmail.com>
- prepare for 0.5
