%global major_version 5.3
Name:           lua
Version:        %{major_version}.1
Release:        2 
Summary:        Powerful light-weight programming language
License:        MIT
URL:            http://www.lua.org/
Source0:        http://www.lua.org/ftp/lua-%{version}.tar.gz
# copied from doc/readme.html on 2014-07-18
Source1:	mit.txt
Patch0:         %{name}-5.3.0-autotoolize.patch
Patch1:         %{name}-5.3.0-idsize.patch
Patch2:         %{name}-5.3.0-luac-shared-link-fix.patch
Patch3:         %{name}-5.2.2-configure-linux.patch
Patch4:		%{name}-5.3.0-configure-compat-module.patch

BuildRequires:  automake autoconf libtool readline-devel ncurses-devel
Provides:       lua(abi) = %{major_version}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package static
Summary:        Static library for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.


%prep
%setup -q 
cp %{SOURCE1} .
mv src/luaconf.h src/luaconf.h.template.in
%patch0 -p1 -E -z .autoxxx
%patch1 -p1 -z .idsize
%patch2 -p1 -z .luac-shared
%patch3 -p1 -z .configure-linux
%patch4 -p1 -z .configure-compat-all
autoreconf -i

%build
%configure --with-readline --with-compat-module
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Autotools give me a headache sometimes.
sed -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{major_version}

%files
%{!?_licensedir:%global license %%doc}
%license mit.txt

%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua
%{_bindir}/luac
%{_libdir}/liblua-%{major_version}.so
%{_mandir}/man1/lua*.1*
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}

%files devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a


%changelog
* Fri Oct 23 2015 cjacker - 5.3.1-2
- Rebuild for new 4.0 release

