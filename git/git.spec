Name: 		git
Version:    	2.6.3
Release: 	2
Summary:  	Core git tools
License: 	GPLv2
URL: 		http://kernel.org/pub/software/scm/git/
Source0: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source1: 	http://kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.xz

Source10:       git@.service
Source11:       git.socket

Patch1:         git-cvsimport-Ignore-cvsps-2.2b1-Branches-output.patch
# http://thread.gmane.org/gmane.comp.version-control.git/266145
# could be removed when update/branch of Michael will be merged in upstream
Patch4:         git-infinite-loop.patch

BuildRequires:	zlib-devel >= 1.2, openssl-devel, expat-devel, gettext, pcre-devel

#for unitdir rpm macros
BuildRequires: systemd-devel

#otherwise perl-Git will provide one.
BuildRequires: perl-Error

Requires:	zlib >= 1.2, libcurl, less, expat
Requires:   git-core = %{version}-%{release}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

%package core
Summary:        Core package of git with minimal funcionality
Requires:       less
Requires:       openssh-clients
Requires:       rsync
Requires:       zlib >= 1.2

%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.

%package daemon
Summary:        Git protocol dæmon
Requires:       git = %{version}-%{release}
Requires:   systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description daemon
The git dæmon for supporting git:// access to git repositories


%package -n perl-Git
Summary:        Perl interface to Git
Requires:       perl(Error)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(ExtUtils::MakeMaker)

%description -n perl-Git
Perl interface to Git.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch4 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS -D_DEFAULT_SOURCE"
%configure \
    --with-openssl \
    --with-libpcre \
    --with-curl \
    --with-expat \
    --with-gitconfig=%{_sysconfdir}/gitconfig \
    --with-gitattributes=%{_sysconfdir}/gitattributes \
    --with-perl \
    --without-python \
    --with-zlib \
    --without-tcltk

make %{?_smp_mflags}
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

#for gitdaemon
mkdir -p %{buildroot}%{_var}/lib/git

#install some helper scripts
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/git

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 0755 ./contrib/completion/git-prompt.sh $RPM_BUILD_ROOT/etc/profile.d


#git installed a lot of same binary with different names in /usr/libexec/git-core/
#we process it.
#GIT_MD5=`md5sum %{buildroot}%{_bindir}/git |awk -F " " '{print $1}'`
#
#for i in `ls %{buildroot}%{_libexecdir}/git-core/*`
#do
#    if [ x"$GIT_MD5" == x"`md5sum $i|awk -F " " '{print $1}'`" ]; then
#        rm -rf $i
#    fi
#done


#install manpages
mkdir -p %{buildroot}%{_mandir}
tar Jxf %{SOURCE1} -C %{buildroot}%{_mandir}

#install systemd unit
mkdir -p %{buildroot}%{_unitdir}/
install -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/
install -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/

#drop some useless perl files.
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

#drop git SVN support
rm -rf %{buildroot}%{_datadir}/perl5/site_perl/Git/SVN
rm -rf %{buildroot}%{_datadir}/perl5/site_perl/Git/SVN.pm
rm -rf %{buildroot}%{_libexecdir}/git-core/git-svn
rm -rf %{buildroot}%{_libexecdir}/git-core/git-remote-testsvn
rm -rf %{buildroot}%{_mandir}/man1/git-svn.1*
rm -rf %{buildroot}%{_mandir}/man3/Git::SVN*

#drop un-used man pages.
rm -rf %{buildroot}%{_mandir}/man1/git-citool.1*
rm -rf %{buildroot}%{_mandir}/man1/git-gui.1*
rm -rf %{buildroot}%{_mandir}/man1/gitk.1*


#drop git CVS server 
rm -rf %{buildroot}%{_mandir}/man1/git-cvsserver.1*
rm -rf %{buildroot}%{_bindir}/git-cvsserver
rm -rf %{buildroot}%{_libexecdir}/git-core/git-cvsserver

#drop gitweb
rm -rf %{buildroot}%{_datadir}/gitweb

# git-archimport is not supported
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'


exclude_re="archimport|email|git-citool|git-cvs|git-daemon|git-gui|git-remote-bzr|git-remote-hg|gitk|p4|svn"
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{_mandir} -type f | grep -vE "$exclude_re|Git" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files

# find translations
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# Split core files
not_core_re="git-(add--interactive|am|difftool|instaweb|relink|request-pull|send-mail|submodule)|gitweb|prepare-commit-msg|pre-rebase"
grep -vE "$not_core_re|\/man\/" bin-man-doc-files > bin-files-core
grep -vE "$not_core_re" bin-man-doc-files | grep "\/man\/" > man-doc-files-core
grep -E "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

%clean
rm -rf $RPM_BUILD_ROOT

%post daemon
%systemd_post git@.service

%preun daemon
%systemd_preun git@.service

%postun daemon
%systemd_postun_with_restart git@.service


%files -f bin-man-doc-git-files 
%defattr(-,root,root)
%{_libexecdir}/git-core/*cvs*
%{_mandir}/man1/git-cvs*

%{_libexecdir}/git-core/*p4*
%{_libexecdir}/git-core/mergetools/p4merge
%{_mandir}/man1/*p4*.1*

%{_libexecdir}/git-core/*email*
%{_mandir}/man1/*email*.1*


%files core -f bin-files-core -f man-doc-files-core
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/git
%{_sysconfdir}/profile.d/*.sh
%{_datadir}/git-core/


%files daemon
%{_unitdir}/git.socket
%{_unitdir}/git@.service
%{_libexecdir}/git-core/git-daemon
%{_mandir}/man1/git-daemon.1*
%{_var}/lib/git


%files -n perl-Git
%defattr(-,root,root)
%{_mandir}/man3/Git.3pm*
%{_mandir}/man3/Git::I18N.3pm*
%{_datadir}/perl5/site_perl/Git.pm
%dir %{_datadir}/perl5/site_perl/Git
%{_datadir}/perl5/site_perl/Git/I18N.pm
%{_datadir}/perl5/site_perl/Git/IndexInfo.pm

%changelog
* Fri Oct 23 2015 cjacker - 2.6.0-2
- Rebuild for new 4.0 release

* Tue Sep 29 2015 Cjacker <cjacker@foxmail.com>
- update to 2.6.0
