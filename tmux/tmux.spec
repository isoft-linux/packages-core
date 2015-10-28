Name: tmux	
Version: 2.0 
Release: 3
Summary: Tool to control multiple terminals from a single terminal 

License: BSD
URL: http://tmux.github.io/
Source0: https://github.com/tmux/tmux/releases/download/%{version}/tmux-%{version}.tar.gz

#default config, almost empty, just set base-index to 1.
Source1:    tmux.conf

#link to libevent static library to avoid introduce libevent in core os.
Source10:   libevent-2.0.18-stable.tar.gz

BuildRequires: gcc
BuildRequires: ncurses-devel
BuildRequires: glibc-devel
 
%description
%{summary}

%prep
%setup -q -a10

%build

pushd libevent-2.0.18-stable
./configure --prefix=`pwd`/../libevent --disable-shared --enable-static
make %{?_smp_mflags}
make install
popd

export PKG_CONFIG_PATH=`pwd`/libevent/lib/pkgconfig

%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/tmux.conf

%files
%config(noreplace) %{_sysconfdir}/tmux.conf
%{_bindir}/tmux
%{_mandir}/man1/tmux.*

%changelog
* Wed Oct 28 2015 Cjacker <cjacker@foxmail.com> - 2.0-3
- Enable mouse scroll by default

* Fri Oct 23 2015 cjacker - 2.0-2
- Rebuild for new 4.0 release

* Wed Aug 19 2015 Cjacker <cjacker@foxmail.com>
- update to 2.0
