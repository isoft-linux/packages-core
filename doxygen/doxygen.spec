Summary: A documentation system for C/C++
Name: doxygen
Version: 1.8.7
Release: 3
Epoch: 1
Url: http://www.stack.nl/~dimitri/doxygen/index.html
Source0: ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz

Patch2: doxygen-we-have-no-latex.patch


License: GPL+

BuildRequires: perl
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%prep
%setup -q 
%patch2 -p1 

%build
unset QTDIR

./configure \
   --prefix %{_prefix} \
   --shared \
   --release

make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} MAN1DIR=share/man/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*


%changelog
* Fri Oct 23 2015 cjacker - 1:1.8.7-3
- Rebuild for new 4.0 release

