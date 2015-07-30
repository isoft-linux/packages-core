%define _without_docs 1
Name: 		git
Version:    2.1.1
Release: 	1
Summary:  	Core git tools
License: 	GPLv2
Group: 		CoreDev/Development/Utility
URL: 		http://kernel.org/pub/software/scm/git/
Source: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source1:	git-init.el
Source2:	git.xinetd
Source3:	git.conf.httpd
Source4:    git.conf.lighttpd
Source5:	gitweb.conf
Patch0:		git-1.5-gitweb-home-link.patch
Patch1:     git-dirty-fix-rpm-wrong-perl-request.patch

BuildRequires:	zlib-devel >= 1.2, openssl-devel, expat-devel, gettext %{!?_without_docs:, xmlto, asciidoc > 6.0.3}
#otherwise perl-Git will provide one.
BuildRequires: perl-Error

Requires:	zlib >= 1.2, libcurl, less, expat
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.3

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          CoreDev/Runtime/Library/Perl
Requires:       perl(Error)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(ExtUtils::MakeMaker)

%description -n perl-Git
Perl interface to Git.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%build
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -D_DEFAULT_SOURCE" \
     ETC_GITCONFIG=/etc/gitconfig \
     gitexecdir=%{_bindir} \
     prefix=%{_prefix} all %{!?_without_docs: doc}

%install
rm -rf $RPM_BUILD_ROOT
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -D_DEFAULT_SOURCE" DESTDIR=$RPM_BUILD_ROOT \
     prefix=%{_prefix} mandir=%{_mandir} \
     ETC_GITCONFIG=/etc/gitconfig \
     gitexecdir=%{_bindir} \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}


#drop git SVN/Gui/Web
rm -rf $RPM_BUILD_ROOT/%{_datadir}/perl5/vendor_perl/Git/SVN
rm -rf $RPM_BUILD_ROOT/%{_datadir}/perl5/vendor_perl/Git/SVN.pm
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-svn
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-archimport
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-cvsexportcommit
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-cvsimport
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-cvsserver
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-daemon
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-gui
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-gui--askpass
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-remote-testsvn
rm -rf $RPM_BUILD_ROOT/%{_bindir}/git-send-email
rm -rf $RPM_BUILD_ROOT/%{_bindir}/gitk
rm -rf $RPM_BUILD_ROOT/%{_datadir}/git-gui
rm -rf $RPM_BUILD_ROOT/%{_datadir}/gitk
rm -rf $RPM_BUILD_ROOT/%{_datadir}/gitweb


find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'
(find $RPM_BUILD_ROOT%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citooli|git-daemon" | sed -e s@^$RPM_BUILD_ROOT@@)               > bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_vendorlib} -type f | sed -e s@^$RPM_BUILD_ROOT@@) >> perl-files

%if %{!?_without_docs:1}0
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool|" | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/git

mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 0755 ./contrib/completion/git-prompt.sh $RPM_BUILD_ROOT/etc/profile.d


rpmclean
%clean
rm -rf $RPM_BUILD_ROOT


%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc README COPYING Documentation/*.txt contrib/hooks
%{!?_without_docs: %doc Documentation/*.html Documentation/docbook-xsl.css}
%{!?_without_docs: %doc Documentation/howto Documentation/technical}
%{_sysconfdir}/bash_completion.d
%{_sysconfdir}/profile.d/*.sh
#%{_libdir}/python*
%{_datadir}/locale/*/LC_MESSAGES/*.mo


%files -n perl-Git -f perl-files
%defattr(-,root,root)

%changelog
