Name:	    tmux	
Version:	1.9a
Release:	1
Summary:	Tool to control multiple terminals from a single terminal 

Group:		Core/Runtime/Utility
License:	BSD
URL:		http://tmux.sourceforge.net
Source0:	%{name}-%{version}.tar.gz

#default config, almost empty, just set base-index to 1.
Source1:    tmux.conf

#link to libevent static library to avoid introduce libevent in core os.
Source10:   libevent-2.0.18-stable.tar.gz

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

rpmclean

%files
%config(noreplace) %{_sysconfdir}/tmux.conf
%{_bindir}/tmux
%{_mandir}/man1/tmux.*

%changelog

