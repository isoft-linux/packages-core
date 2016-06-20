#Do not provide any elf.
%define debug_package %{nil}

Name: libclc
Version: 0.2.0
Release: 16.255421.svn
Epoch: 2 
Summary: An open source implementation of the OpenCL 1.1 library requirements
License: BSD
URL: http://libclc.llvm.org/

Source0: libclc.tar.xz
# Only builds on x86
ExclusiveArch:	%{ix86} x86_64

BuildRequires: libclang-devel
BuildRequires: libedit-devel
BuildRequires: libllvm-devel >= 3.7.0
BuildRequires: libllvm-static
BuildRequires: python
BuildRequires: zlib-devel
BuildRequires: git

%description
libclc is an open source, BSD licensed implementation of the library
requirements of the OpenCL C programming language, as specified by the
OpenCL 1.1 Specification. 

libclc is intended to be used with the Clang compiler's OpenCL frontend.

libclc is designed to be portable and extensible. To this end, it provides
generic implementations of most library requirements, allowing the target
to override the generic implementation at the granularity of individual
functions.

libclc currently only supports the PTX target, but support for more
targets is welcome.


%package devel
Summary: Development files for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libclc

%build
CFLAGS="%{optflags} -D__extern_always_inline=inline"
./configure.py --prefix=%{_prefix} --libexecdir=%{_libdir}/clc/ --pkgconfigdir=%{_libdir}/pkgconfig/

# fstack-protector-strong is currently not supported by clang++
sed -i "s/fstack-protector-strong/fstack-protector/" Makefile

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%doc LICENSE.TXT README.TXT CREDITS.TXT
%{_libdir}/clc/*.bc
%{_includedir}/clc

%files devel
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Dec 12 2015 Cjacker <cjacker@foxmail.com> - 2:0.2.0-16.255421.svn
- Update and rebuild

* Sat Dec 05 2015 Cjacker <cjacker@foxmail.com> - 2:0.2.0-12.llvm37.svn20151205
- Update

* Tue Oct 27 2015 Cjacker <cjacker@foxmail.com> - 2:0.2.0-11.llvm37.git20150727
- Rebuild

* Sat Oct 17 2015 Cjacker <cjacker@foxmail.com>
- rebuild.

* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- update to 0.2.0 git.
- requires llvm>=3.7.0

* Fri Jul 10 2015 Cjacker <cjacker@foxmail.com>
- checkout 0.1.0 revision and build with clang-3.6.1
