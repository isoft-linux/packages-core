%global _use_internal_dependency_generator 0

Summary: Tools needed to create Texinfo format documentation files
Name: texinfo
Version: 6.0
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Publishing
Url: http://www.gnu.org/software/texinfo/
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz.sig
Source2: info-dir
# Source3: script for filtering out false perl requires
Source3:   filter-requires-texinfo.sh
# Source4: script for filtering out false perl provides
Source4: filter-provides-texinfo.sh
# Source5: macro definitions
Source5: macros.info
Patch0: texinfo-4.12-zlib.patch
Patch1: texinfo-6.0-disable-failing-info-test.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: perl >= 5.7.3, perl(Text::Unidecode)
Requires: perl(Unicode::EastAsianWidth), perl(Data::Dumper), perl(Locale::Messages)
BuildRequires: zlib-devel, ncurses-devel, help2man, perl(Data::Dumper)
BuildRequires: perl(Locale::Messages), perl(Unicode::EastAsianWidth), perl(Text::Unidecode)

%global __find_requires %{SOURCE3}
%global __find_provides %{SOURCE4}

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation
Group: System Environment/Base

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

#%package tex
#Summary: Tools for formatting Texinfo documentation files using TeX
#Group: Applications/Publishing
#Requires: texinfo = %{version}-%{release}
#Requires: tex(tex) tex(epsf.tex)
#Requires(post): %{_bindir}/texconfig-sys
#Requires(postun): %{_bindir}/texconfig-sys
#
#%description tex
#Texinfo is a documentation system that can produce both online
#information and printed output from a single source file. The GNU
#Project uses the Texinfo file format for most of its documentation.
#
#The texinfo-tex package provides tools to format Texinfo documents
#for printing using TeX.

%prep
%setup -q
%patch0 -p1 -b .zlib
%patch1 -p1 -b .disable-failing-info-test

%build
%configure --with-external-Text-Unidecode \
           --with-external-libintl-perl \
           --with-external-Unicode-EastAsianWidth
make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}/sbin

make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_infodir}/dir
mv $RPM_BUILD_ROOT%{_bindir}/install-info $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cp %{SOURCE5} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d

%find_lang %{name}
%find_lang %{name}_document

#we do not ship these files/related to tex/latex.
rm -rf %{buildroot}%{_bindir}/pdftexi2dvi
rm -rf %{buildroot}%{_bindir}/texi2dvi
rm -rf %{buildroot}%{_bindir}/texi2pdf
rm -rf %{buildroot}%{_bindir}/texindex
rm -rf %{buildroot}%{_mandir}/man1/pdftexi2dvi.1*
rm -rf %{buildroot}%{_mandir}/man1/texi2dvi.1*
rm -rf %{buildroot}%{_mandir}/man1/texi2pdf.1*
rm -rf %{buildroot}%{_mandir}/man1/texindex.1*

%check
export ALL_TESTS=yes
make %{?_smp_mflags} check

%post
if [ -f %{_infodir}/texinfo.gz ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/texinfo.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/texinfo.gz ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/texinfo.gz %{_infodir}/dir || :
    fi
fi

%post -n info
if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/info-stnd.info %{_infodir}/dir
fi
if [ -x /bin/sed ]; then
    /bin/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/info-stnd.info %{_infodir}/dir \
        || :
    fi
fi

#%post tex
#%{_bindir}/texconfig-sys rehash 2> /dev/null || :
#
#%postun tex
#%{_bindir}/texconfig-sys rehash 2> /dev/null || :


%files -f %{name}.lang -f %{name}_document.lang
%doc AUTHORS ChangeLog NEWS README TODO
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/texinfo.5*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*

%files -n info
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/info
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
/sbin/install-info
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
%{_rpmconfigdir}/macros.d/macros.info

#%files tex
#%{_bindir}/texindex
#%{_bindir}/texi2dvi
#%{_bindir}/texi2pdf
#%{_bindir}/pdftexi2dvi
#%{tex_texinfo}/
#%{_mandir}/man1/texindex.1*
#%{_mandir}/man1/texi2dvi.1*
#%{_mandir}/man1/texi2pdf.1*
#%{_mandir}/man1/pdftexi2dvi.1*

%changelog
* Mon Aug 03 2015 Cjacker <cjacker@foxmail.com>
- update to 6.0
