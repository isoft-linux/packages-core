%define withvimspell 0
%define withhunspell 0

%define baseversion 7.4
#should as same as Source1
%define patchlevel 796
%define vimdir vim74

Summary: The VIM editor
URL:     http://www.vim.org/
Name:    vim
Version: %{baseversion}.%{patchlevel}
Release: 9
License: GPL
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}.tar.bz2
#from ftp://ftp.vim.org/pub/vim/patches/7.4/
#download all patches and tar them.
Source1: vim-patches.tar.gz

Source2: vimrc

Source10: new-rpm-spec-syntax.vim
 
Source20: spec-template.new
 
%if %{withvimspell}
Source14: vim-spell-files.tar.bz2
%endif

Patch2002: vim-7.0-fixkeys.patch
%if %{withhunspell}
Patch2011: vim-7.0-hunspell.patch
BuildRequires: hunspell-devel
%endif

Patch3002: vim-6.1-rh2.patch
Patch3003: vim-6.1-rh3.patch
Patch3004: vim-7.0-rclocation.patch
Patch3009: vim-7.0-warning.patch
Patch3010: vim-7.0-syncolor.patch
Patch3012: vim-7.0-specedit.patch
Patch3013: vim-add-vala.patch

BuildRequires: ncurses-devel gettext

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%prep
%setup -q  -n %{vimdir} -a1

for i in `ls vim-patches/7.4.*`
do
    cat $i|patch -p0
done 

#update rpm spec syntax highlight defines...
rm -rf runtime/syntax/spec.vim
cp -r %{SOURCE10} runtime/syntax/spec.vim

%patch2002 -p1

%if %{withhunspell}
%patch2011 -p1
%endif

perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE14}
%endif

%patch3002 -p1
%patch3003 -p1
%patch3004 -p1

%patch3009 -p1
%patch3010 -p1
%patch3012 -p1
%patch3013 -p1

%build

rm -rf mini
cp -r src mini
#build a minimum vi
cd mini
%configure \
        --with-features=small \
        --enable-multibyte \
        --without-x \
        --disable-nls \
        --disable-netbeans \
        --disable-gui \
        --disable-perlinterp \
        --disable-pythoninterp \
        --disable-tclinterp \
        --disable-gpm
make %{?_smp_mflags}
cd ..

#build vim with python/perl support.
cd src
%configure \
        --with-features=huge \
        --without-x \
        --enable-multibyte \
        --enable-gui=no \
        --enable-perlinterp=yes \
        --enable-pythoninterp=dynamic \
        --enable-luainterp=dynamic \
        --disable-tclinterp \
        --disable-netbeans \
        --enable-gpm
make %{?_smp_mflags}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

cd src
make install DESTDIR=$RPM_BUILD_ROOT
make installmacros DESTDIR=$RPM_BUILD_ROOT

#install spec template
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/
cp -f %{SOURCE20} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec

mkdir -p $RPM_BUILD_ROOT/etc
install -m0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/vimrc

#remove this files, do not import unneeded dependencies
rm -rf $RPM_BUILD_ROOT%{_datadir}/vim/vim74/tools

#alias vi to vim, that's to say, use vim as vi in common.
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh <<EOF
alias vi=vim
EOF
chmod 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh

cd .. # from src

#install the mini vi
install -m0755 mini/vim $RPM_BUILD_ROOT%{_bindir}/vi

#remove localized man page.
rm -rf $RPM_BUILD_ROOT%{_mandir}/{fr.ISO8859-1, fr.UTF-8, fr, it.ISO8859-1}
rm -rf $RPM_BUILD_ROOT%{_mandir}/{it.UTF-8, it, ja, pl.ISO8859-1, pl.UTF-8, pl}
rm -rf $RPM_BUILD_ROOT%{_mandir}/{ru.KOI8-R, ru.UTF-8}


%postun
if [ -x /usr/bin/busybox ]; then
    /usr/bin/busybox --install -s
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/profile.d/vim.sh
%{_sysconfdir}/vimrc
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/vim
%{_datadir}/vim/*

%changelog
* Fri Oct 23 2015 cjacker - 7.4.796-9
- Rebuild for new 4.0 release

