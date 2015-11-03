Name: asciidoc		
Version: 8.6.9	
Release: 3
Summary: Text document format for short documents, articles, books and UNIX man pages
License: GPL
URL: http://www.methods.co.nz/asciidoc/
Source0: http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/%{name}-%{version}.tar.gz
Patch0: 0001-a2x-Write-manifests-in-UTF-8-by-default.patch

#we used in in build, but do not want ship it in our os.
Source10: http://ibiblio.org/pub/Linux/utils/file/symlinks-1.4.tar.gz
Patch11: symlinks-coverity-readlink.patch
Patch12: symlinks-coverity-overrun-dynamic.patch

BuildRequires: python2-devel
BuildRequires: libxslt

Requires: python, libxslt	

BuildArch: noarch

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.


%prep
%setup -q -a10
%patch0 -p1

cd symlinks-1.4
%patch11 -p1
%patch12 -p1


%build
#first build internal symlinks
pushd symlinks-1.4
make
popd

%configure
make %{?_smp_mflags}

%install
make install docs DESTDIR=%{buildroot}

install -dm 755 %{buildroot}%{_datadir}/asciidoc/
# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets; do
    mv -v %{buildroot}%{_sysconfdir}/asciidoc/$d \
          %{buildroot}%{_datadir}/asciidoc/
    # absolute symlink into buildroot is intentional, see below
    ln -s %{buildroot}%{_datadir}/%{name}/$d %{buildroot}%{_sysconfdir}/%{name}/

    # let's symlink stuff for documentation as well so we don't duplicate things
    rm -rf %{buildroot}%{_docdir}/%{name}/$d
    # absolute symlink into buildroot is intentional, see below
    ln -s %{buildroot}%{_datadir}/%{name}/$d %{buildroot}%{_docdir}/%{name}/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

mkdir -p %{buildroot}%{_datadir}/vim/vimfiles/{ftdetect,syntax}
for file in $(cd vim; find * -type f); do
    install -m 0644 vim/$file %{buildroot}%{_datadir}/vim/vimfiles/$file
done

# Absolute symlinks were used above to be able to detect dangling ones. Make
# them relative now (sane for being installed) and remove dangling symlinks.
./symlinks-1.4/symlinks -cdr %{buildroot}

%check
export PATH="../:$PATH"
cd tests
python testasciidoc.py update
python testasciidoc.py run


%files
%_pkgdocdir

%dir %{_sysconfdir}/asciidoc
%{_sysconfdir}/asciidoc/*
%{_bindir}/a2x
%{_bindir}/a2x.py
%{_bindir}/asciidoc
%{_bindir}/asciidoc.py
%{_datadir}/asciidoc
%{_datadir}/vim/vimfiles/syntax/asciidoc.vim
%{python_sitelib}/*

%{_mandir}/man1/a2x.1.gz
%{_mandir}/man1/asciidoc.1.gz


%changelog
* Tue Nov 03 2015 Cjacker <cjacker@foxmail.com> - 8.6.9-3
- install data files to /usr/share instead of /etc

* Fri Oct 23 2015 cjacker - 8.6.9-2
- Rebuild for new 4.0 release
