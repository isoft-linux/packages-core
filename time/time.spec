Summary: A GNU utility for monitoring a program's use of system resources
Name: time
Version: 1.7
Release: 48
License: GPLv2+
Group: Applications/System
Url: http://www.gnu.org/software/time/
Source: ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Patch0: time-1.7-destdir.patch
Patch1: time-1.7-verbose.patch
# Bug #702826
Patch2: time-1.7-ru_maxrss-is-in-kilobytes-on-Linux.patch
# Bug #527276
Patch3: time-1.7-Recompute-CPU-usage-at-microsecond-level.patch

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running, and displays
the results.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .ru_maxrss
%patch3 -p1 -b .recompute_cpu

%build
echo "ac_cv_func_wait3=\${ac_cv_func_wait3='yes'}" >> config.cache
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

%files
%{_bindir}/time

%changelog
