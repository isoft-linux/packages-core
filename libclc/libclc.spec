Name:           libclc
Version:        0.1.0
Release:        10.git20150710
Summary:        An open source implementation of the OpenCL 1.1 library requirements
License:        BSD
URL:            http://libclc.llvm.org/
#git clone http://llvm.org/git/libclc.git
Source0:        libclc.tar.gz
Patch0: libclc-fix-build-with-llvm-3.6.1.patch
# Only builds on x86
ExclusiveArch:	%{ix86} x86_64

BuildRequires:  libclang-devel
BuildRequires:  libedit-devel
BuildRequires:  libllvm-devel
BuildRequires:  libllvm-static
BuildRequires:  python
BuildRequires:  zlib-devel
BuildRequires:  git
%description
libclc is an open source, BSD licensed implementation of the library
requirements of the OpenCL C programming language, as specified by the
OpenCL 1.1 Specification. The following sections of the specification
impose library requirements:

  * 6.1: Supported Data Types
  * 6.2.3: Explicit Conversions
  * 6.2.4.2: Reinterpreting Types Using as_type() and as_typen()
  * 6.9: Preprocessor Directives and Macros
  * 6.11: Built-in Functions
  * 9.3: Double Precision Floating-Point
  * 9.4: 64-bit Atomics
  * 9.5: Writing to 3D image memory objects
  * 9.6: Half Precision Floating-Point

libclc is intended to be used with the Clang compiler's OpenCL frontend.

libclc is designed to be portable and extensible. To this end, it provides
generic implementations of most library requirements, allowing the target
to override the generic implementation at the granularity of individual
functions.

libclc currently only supports the PTX target, but support for more
targets is welcome.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libclc
#Revision 225041 - Directory Listing
#Modified Wed Dec 31 09:27:53 2014 CST (6 months, 1 week ago) by tstellar
#
#Require LLVM 3.6 and bump version to 0.1.0
#
#Some functions are implemented using hand-written LLVM IR, and
#LLVM assembly format is allowed to change between versions, so we
#should require a specific version of LLVM.
git checkout 9a53500b66544d50b0f42afa4eb0de3b6cdbcb16

%patch0 -p1

%build
CFLAGS="%{optflags} -D__extern_always_inline=inline"
./configure.py --prefix=%{_prefix} --libexecdir=%{_libdir}/clc/ --pkgconfigdir=%{_libdir}/pkgconfig/

# fstack-protector-strong is currently not supported by clang++
sed -i "s/fstack-protector-strong/fstack-protector/" Makefile

make %{?_smp_mflags}


%install
%make_install


%files
%doc LICENSE.TXT README.TXT CREDITS.TXT
%{_libdir}/clc/*.bc
%{_includedir}/clc

%files devel
%doc
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Jul 10 2015 cjacker <cjacker@foxmail.com>
- checkout 0.1.0 revision and build with clang-3.6.1
