# we ship this package but disabled by default.
# bash_completion is slow and has some strange behaviors about completion.
%bcond_with tests
# The *.py files we ship are not python scripts, #813651
%global _python_bytecompile_errors_terminate_build 0

Name:           bash-completion
Version:        2.1
Release:        10.git
Epoch:          1
Summary:        Programmable completion for Bash

License:        GPLv2+
URL:            http://bash-completion.alioth.debian.org/
# git clone git://git.debian.org/git/bash-completion/bash-completion.git
Source0:        http://bash-completion.alioth.debian.org/files/%{name}.tar.gz
Patch0:         %{name}-1.99-noblacklist.patch

BuildArch:      noarch
%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
%endif
# For Patch1
BuildRequires:  automake
BuildRequires:  sed

Requires:       bash >= 4.1

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.


%prep
%setup -q -n %{name}
%patch0 -p1
autoreconf -ivf # for patch1

%build
%configure
make %{?_smp_mflags}

cat <<EOF >redefine_filedir

# This is a copy of the _filedir function in bash_completion, included
# and (re)defined separately here because some versions of Adobe
# Reader, if installed, are known to override this function with an
# incompatible version, causing various problems.
#
# http://forums.adobe.com/thread/745833

EOF
sed -ne '/^_filedir\s*(/,/^}/p' bash_completion >>redefine_filedir


%install
make install DESTDIR=$RPM_BUILD_ROOT
install -Dpm 644 redefine_filedir \
    $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/redefine_filedir

# Updated completion shipped in cowsay package:
rm $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/{cowsay,cowthink}

#disable it, add # to everyline of %{_sysconfdir}/profile.d/bash_completion.sh
sed -i 's/^/#&/g' %{buildroot}%{_sysconfdir}/profile.d/bash_completion.sh

%if %{with tests}
%check
# For some tests involving non-ASCII filenames
export LANG=en_US.UTF-8
# This stuff borrowed from dejagnu-1.4.4-17 (tests need a terminal)
tmpfile=$(mktemp)
screen -D -m sh -c '( make check ; echo $? ) >'$tmpfile
cat $tmpfile
result=$(tail -n 1 $tmpfile)
rm -f $tmpfile
exit $result
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS CHANGES README doc/bash_completion.txt
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/
%{_datadir}/bash-completion/
%{_datadir}/cmake/
%{_datadir}/pkgconfig/bash-completion.pc


%changelog
