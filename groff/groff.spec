%define with_x 0

Summary: A document formatting system
Name: groff
Version: 1.22.3
Release: 2
License: GPLv3+ and GFDL and BSD and MIT
URL: http://groff.ffii.org

Source0: ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
Requires: mktemp
Provides: nroff-i18n = %{version}-%{release}

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-x11 package.

%package perl
Summary: Parts of the groff formatting system that require Perl
Requires: groff = %{version}-%{release}
%global __requires_exclude ^perl\\([^.]*\\.pl\\)

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit (font processor
for creating PostScript font files), groffer (tool for displaying groff
files), grog (utility that can be used to automatically determine groff
command-line options), chem (groff preprocessor for producing chemical
structure diagrams), mmroff (reference preprocessor) and roff2dvi
roff2html roff2pdf roff2ps roff2text roff2x (roff code converters).

%if %{with_x}
%package x11
Summary: Parts of the groff formatting system that require X Windows System
BuildRequires: libXaw-devel libXmu-devel
Requires: groff = %{version}-%{release}
Provides: groff-gxditview = %{version}-%{release}
Obsoletes: groff-gxditview < 1.20.1


%description x11
The groff-x11 package contains the parts of the groff text processor
package that require X Windows System. These include gxditview (display
groff intermediate output files on X Window System display) and
xtotroff (converts X font metrics into groff font metrics).
%endif

%prep
%setup -q

%build
%configure \
	--docdir=%{_docdir}/%{name}-%{version} \
	--with-appresdir=%{_datadir}/X11/app-defaults \
	--with-grofferdir=%{_datadir}/%{name}/%{version}/groffer \
    --without-x
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# some binaries need alias with 'g' or 'z' prefix

for file in g{nroff,troff,tbl,pic,eqn,neqn,refer,lookbib,indxbib,soelim} zsoelim; do
	ln -s ${file#?} %{buildroot}%{_bindir}/${file}
	ln -s ${file#?}.1.gz %{buildroot}%{_mandir}/man1/${file}.1.gz
done

# perl dependent files in /usr/bin will be in separate package

rm -f files-perl files-nonperl
for file in %{buildroot}%{_bindir}/*; do
	# package selection
	if grep -q -m1 '^#!.*\<perl\>' $file; then
		output_file=files-perl
	else
		output_file=files-nonperl
	fi

	echo %{_bindir}/$(basename $file) >> $output_file

	# manpage availability
	manfile=%{buildroot}%{_mandir}/man1/$(basename $file).\*
	if [ -f $manfile -o -L $manfile ]; then
		echo %{_mandir}/man1/$(basename $file).\* >> $output_file
	fi
done
# rename groff downloadable postscript fonts
# these files are more PS instructions, than general-purpose fonts (bz #477394)

for file in $(find %{buildroot}%{_datadir}/%{name}/%{version}/font/devps -name "*.pfa"); do
	mv ${file} ${file}_
done

sed --in-place 's/\.pfa$/.pfa_/' %{buildroot}%{_datadir}/%{name}/%{version}/font/devps/download

# remove unnecessary files and fix privileges

rm -rf %{buildroot}%{_infodir}

# we do not ship docs that nobody read, just go to web and search how to use groff.
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}

chmod 755 %{buildroot}%{_datadir}/groff/%{version}/groffer/version.sh
chmod 755 %{buildroot}%{_datadir}/groff/%{version}/font/devlj4/generate/special.awk


%clean
rm -rf %{buildroot}


%files -f files-nonperl
%defattr(-,root,root,-)
%{_libdir}/groff/groff_opts_no_arg.txt
%{_libdir}/groff/groff_opts_with_arg.txt
%{_libdir}/groff/grog/subs.pl
%{_datadir}/groff/
# manpages for binaries are covered by -f
%{_mandir}/man1/grohtml.*
%{_mandir}/man5/*
%{_mandir}/man7/*
%exclude %{_datadir}/groff/%{version}/groffer
%if %{with_x}
%exclude %{_bindir}/gxditview
%exclude %{_bindir}/xtotroff
%exclude %{_mandir}/man1/gxditview.*
%exclude %{_mandir}/man1/xtotroff.*
%endif

%files perl -f files-perl
%defattr(-,root,root,-)
%{_datadir}/groff/%{version}/groffer/
%{_libdir}/groff/glilypond/args.pl
%{_libdir}/groff/glilypond/oop_fh.pl
%{_libdir}/groff/glilypond/subs.pl
%{_libdir}/groff/gpinyin/subs.pl

%if %{with_x}
%files x11
%defattr(-,root,root,-)
%{_bindir}/gxditview
%{_bindir}/xtotroff
%{_datadir}/X11/app-defaults/GXditview
%{_datadir}/X11/app-defaults/GXditview-color
%{_mandir}/man1/gxditview.*
%{_mandir}/man1/xtotroff.*
%endif

%changelog
* Mon Dec 19 2016 sulit - 1.22.3-2
- remove perl(*.pl) dependences

* Thu Dec 15 2016 sulit - 1.22.3-1
- upgrade groff to 1.22.3

* Fri Oct 23 2015 cjacker - 1.22.2-4
- Rebuild for new 4.0 release

