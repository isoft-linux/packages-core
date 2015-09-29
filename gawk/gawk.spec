Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 4.1.3
Release: 2 
License: GPL
Group:  Core/Runtime/Utility 
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz

Requires: /bin/mktemp
Provides: /bin/awk
Provides: /bin/gawk

%description
The gawk packages contains the GNU version of awk, a text processing
utility. Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%package        devel
Summary:        gawk extension development header
Group:          Development/Libraries

%description    devel
gawk extension development header

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=${RPM_BUILD_ROOT}/%{_bindir} \
	libexecdir=${RPM_BUILD_ROOT}%{_libexecdir} \
	datadir=${RPM_BUILD_ROOT}%{_datadir}

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf gawk.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/awk.1.gz
rm -f $RPM_BUILD_ROOT/%{_bindir}/{,p}gawk-%{version}

rm -rf $RPM_BUILD_ROOT%{_infodir}

%find_lang %name

rpmclean

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang 
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%{_libexecdir}/awk
%{_datadir}/awk
%{_libdir}/gawk/*.so
%{_mandir}/man3/*.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/gawkapi.h

%changelog
