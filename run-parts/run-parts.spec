Name:	    run-parts	
Version:	4.4
Release:	2
Summary:	Run scripts or programs in a directory

License:	GPL
URL:		http://packages.qa.debian.org/d/debianutils.html
Source0:	ftp://ftp.archlinux.org/other/run-parts/debianutils_4.4.tar.gz

%description
%{summary}

%prep
%setup -q -n debianutils-%{version} 

%build
%configure

make %{?_smp_mflags} run-parts


%install
install -D -m0755 run-parts $RPM_BUILD_ROOT%{_bindir}/run-parts
install -D -m0644 run-parts.8 $RPM_BUILD_ROOT%{_mandir}/man8/run-parts.8


%postun
#busybox also provide this applet, if it exists and this package was removed,
#use busybox to re-create the command.
#but we had no need to setup this package depend on busybox.
if [ -x /usr/bin/busybox ]; 
then 
    /usr/bin/busybox --install -s
fi

%files
%{_bindir}/run-parts
%{_mandir}/man8/*.gz

%changelog
* Fri Oct 23 2015 cjacker - 4.4-2
- Rebuild for new 4.0 release

