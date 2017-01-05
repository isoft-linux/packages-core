Summary: A documentation system for C/C++
Name: doxygen
Version: 1.8.13
Release: 1
Epoch: 1
Url: http://www.stack.nl/~dimitri/doxygen/index.html
Source0: ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
License: GPL+

BuildRequires: perl
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison
BuildRequires: cmake
BuildRequires: xapian-core-devel

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%prep
%setup -q 
# convert into utf-8
iconv --from=ISO-8859-1 --to=UTF-8 LANGUAGE.HOWTO > LANGUAGE.HOWTO.new
touch -r LANGUAGE.HOWTO LANGUAGE.HOWTO.new
mv LANGUAGE.HOWTO.new LANGUAGE.HOWTO

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
      -Dbuild_doc=OFF \
      -Dbuild_wizard=ON \
      -Dbuild_xmlparser=ON \
      -Dbuild_search=ON \
      -DMAN_INSTALL_DIR=%{_mandir}/man1 \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DBUILD_SHARED_LIBS=OFF \
      ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

# install man pages
mkdir -p %{buildroot}/%{_mandir}/man1
cp doc/*.1 %{buildroot}/%{_mandir}/man1/

# remove duplicate
rm -rf %{buildroot}/%{_docdir}/packages

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/doxygen
%{_bindir}/doxyindexer
%{_bindir}/doxysearch.cgi
%{_bindir}/doxywizard
%{_mandir}/man1/doxyindexer.1.gz
%{_mandir}/man1/doxysearch.1.gz
%{_mandir}/man1/doxywizard.1.gz
%{_mandir}/man1/doxygen.1*


%changelog
* Thu Jan 05 2017 sulit - 1:1.8.13-1
- upgrade doxygen to 1.8.13

* Fri Oct 23 2015 cjacker - 1:1.8.7-3
- Rebuild for new 4.0 release

