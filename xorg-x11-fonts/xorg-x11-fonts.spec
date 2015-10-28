#we only provide misc fonts in this package.


%define _x11fontdirprefix	%{_datadir}
%define _x11fontdir		%{_x11fontdirprefix}/fonts/X11

Summary:	X.Org X11 basic fonts
Name:		xorg-x11-fonts
Version:	7.5
Release:	4
License:	Various licenses
URL:		http://www.x.org

BuildArch:	noarch

Source0: 	encodings-1.0.3.tar.bz2	
Source1:	font-alias-1.0.2.tar.bz2

Source2:	font-cursor-misc-1.0.1.tar.bz2
Source3:	font-dec-misc-1.0.1.tar.bz2
Source4:	font-isas-misc-1.0.1.tar.bz2
Source5:	font-jis-misc-1.0.1.tar.bz2
Source6:	font-micro-misc-1.0.1.tar.bz2
Source7:	font-misc-misc-1.1.0.tar.bz2
Source8:	font-mutt-misc-1.0.1.tar.bz2
Source9:	font-schumacher-misc-1.1.0.tar.bz2
Source10:	font-sony-misc-1.0.1.tar.bz2
Source11:	font-sun-misc-1.0.1.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: ucs2any, bdftruncate, bdftopcf
BuildRequires: perl

%description
X.Org X Window System fonts

%package base
Summary: Base fonts required by the X Window System.
Requires(post): mkfontdir, mkfontscale, fontconfig
Requires(postun): mkfontdir, mkfontscale, fontconfig
# Required so upgrades work, since base fonts moved here from main pkg
Conflicts: XFree86 <= 4.2.0-3.1
# The fonts.* files from truetype and syriac moved from those pkgs to base
Conflicts: XFree86-truetype-fonts < 4.2.99.901-20030209.2
Conflicts: XFree86-syriac-fonts < 4.2.99.901-20030209.2

%description base
This package provides the base fonts, and font encoding files that are
required by the X Window System.

%package misc
Summary: misc bitmap fonts for the X Window System
Requires(post): mkfontdir, fontconfig
Requires(postun): mkfontdir, fontconfig

%description misc
This package contains misc bitmap Chinese, Japanese, Korean, Indic, and Arabic
fonts for use with X Window System.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11

%build
for dir in $(find . -maxdepth 1 -type d -name '[a-z]*-[0-9]*' | sort | sed -e 's#\./##g') ; do
    pushd $dir
    case $dir in
        encodings-*)
            perl -p -i -e 's#(^DEFAULT(_|_OTF|_TTF)FONTDIR=)\${libdir}/X11/fonts#\1\$(pkg-config --variable=fontdir fontutil)#' configure.ac
            autoconf
            %configure
        ;;

        *)
            # FIXME: Yes, this perl hack is fairly ugly, but beats the heck out of
            # making a patch that patches 35 or so configure.ac files and maintaining
            # it for an indefinite amount of time.  Hopefully my solution here will
            # get considered to be included in upstream 7.1 release in which case I'll
            # turn it into a series of diffs instead and submit it.  For now tho, perl
            # is my friend.  -- mharris
            perl -p -i -e 's#(^DEFAULT(_|_OTF|_TTF)FONTDIR=)\${libdir}/X11/fonts#\1\$(pkg-config --variable=fontdir fontutil)#' configure.ac
            autoconf
            %configure \
                --disable-iso8859-3 --disable-iso8859-4 --disable-iso8859-6 \
                --disable-iso8859-10 --disable-iso8859-11 --disable-iso8859-12 \
                --disable-iso8859-13 --disable-iso8859-16
        ;;
    esac

    make
    popd
done

#--------------------------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT

for dir in $(find . -maxdepth 1 -type d -name '[a-z]*-[0-9]*' | sort | sed -e 's#\./##g') ; do
    pushd $dir
    # FIXME: The upstream sources need to be patched to allow direct
    # specification of the 'fontdir' variable, instead of it being
    # relative to libdir.
    make install DESTDIR=$RPM_BUILD_ROOT
    popd
done

# Create fake %ghost files for file manifests.
{
    # Make ghost fonts.alias, fonts.dir, encodings.dir files
    FONTDIR=$RPM_BUILD_ROOT%{_x11fontdir}
    # Create fake %ghost fonts.alias
    # Create fake %ghost encodings.dir, fonts.dir, fonts.cache-*
    for subdir in misc ; do
        rm -f $FONTDIR/$subdir/{encodings,fonts}.dir
        touch $FONTDIR/$subdir/{encodings,fonts}.dir
        chmod 0644 $FONTDIR/$subdir/{encodings,fonts}.dir

        # Create bogus fonts.cache-* files
        # Create somewhat future-proofed ghosted fonts.cache-* files so that
        # the font packages own these files.
        for fcver in $(seq 1 9) ; do
            touch $FONTDIR/$subdir/fonts.cache-$fcver
            chmod 0644 $FONTDIR/$subdir/fonts.cache-$fcver
        done
    done
}

#delete empty dirs.
rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts/X11/100dpi
rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts/X11/75dpi
rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts/X11/cyrillic

%post base
{
  FONTDIR=%{_x11fontdir}/misc
  ENCODINGSDIR=%{_datadir}/fonts/X11/encodings
  #-------------------------------------------------------------------
  # Both installs and upgrades
  {
	pushd "${ENCODINGSDIR}"
    mkfontscale -n -e "${ENCODINGSDIR}" -e large
	popd &> /dev/null
  }

  mkfontdir $FONTDIR 
  # NOTE: We add the ":unscaled" suffix to avoid ugly bitmap fonts.
  fc-cache $FONTDIR
}

%postun base
{
  if [ "$1" = "0" ]; then
    mkfontdir %{_x11fontdir}/misc
    fc-cache %{_x11fontdir}/misc
  fi
}

%post misc
{
  FONTDIR=%{_x11fontdir}/misc
  mkfontdir $FONTDIR 
  fc-cache $FONTDIR
}

%postun misc
{
  # Rebuild fonts.dir when uninstalling package. (exclude the local, CID dirs)
  if [ "$1" = "0" ]; then
    mkfontdir %{_x11fontdir}/misc
    fc-cache %{_x11fontdir}/misc
  fi
}

%clean
rm -rf $RPM_BUILD_ROOT

%files base
%defattr(-,root,root,-)
%dir %{_x11fontdir}
%dir %{_x11fontdir}/misc
# font-cursor-misc 	('cursor' font required by X server)
%{_x11fontdir}/misc/cursor.pcf*
# font-dec-misc		(DEC cursors)
%{_x11fontdir}/misc/dec????.pcf*
# font-misc-misc	('fixed' font required by X server)
%{_x11fontdir}/misc/[1-9]*-ISO8859-*.pcf*
%{_x11fontdir}/misc/10x20-KOI8-R.pcf*
%{_x11fontdir}/misc/10x20.pcf*
%{_x11fontdir}/misc/12x13ja.pcf*
%{_x11fontdir}/misc/18x18ja.pcf*
%{_x11fontdir}/misc/18x18ko.pcf*
%{_x11fontdir}/misc/4x6-KOI8-R.pcf*
%{_x11fontdir}/misc/4x6.pcf*
%{_x11fontdir}/misc/5x7-KOI8-R.pcf*
%{_x11fontdir}/misc/5x7.pcf*
%{_x11fontdir}/misc/5x8-KOI8-R.pcf*
%{_x11fontdir}/misc/5x8.pcf*
%{_x11fontdir}/misc/6x10-KOI8-R.pcf*
%{_x11fontdir}/misc/6x10.pcf*
%{_x11fontdir}/misc/6x12-KOI8-R.pcf*
%{_x11fontdir}/misc/6x12.pcf*
%{_x11fontdir}/misc/6x13-KOI8-R.pcf*
%{_x11fontdir}/misc/6x13.pcf*
%{_x11fontdir}/misc/6x13B.pcf*
%{_x11fontdir}/misc/6x13O.pcf*
%{_x11fontdir}/misc/6x9-KOI8-R.pcf*
%{_x11fontdir}/misc/6x9.pcf*
%{_x11fontdir}/misc/7x13-KOI8-R.pcf*
%{_x11fontdir}/misc/7x13.pcf*
%{_x11fontdir}/misc/7x13B.pcf*
%{_x11fontdir}/misc/7x13O.pcf*
%{_x11fontdir}/misc/7x14-JISX0201.1976-0.pcf*
%{_x11fontdir}/misc/7x14-KOI8-R.pcf*
%{_x11fontdir}/misc/7x14.pcf*
%{_x11fontdir}/misc/7x14B.pcf*
%{_x11fontdir}/misc/8x13-KOI8-R.pcf*
%{_x11fontdir}/misc/8x13.pcf*
%{_x11fontdir}/misc/8x13B.pcf*
%{_x11fontdir}/misc/8x13O.pcf*
%{_x11fontdir}/misc/9x15-KOI8-R.pcf*
%{_x11fontdir}/misc/9x15.pcf*
%{_x11fontdir}/misc/9x15B.pcf*
%{_x11fontdir}/misc/9x18-KOI8-R.pcf*
%{_x11fontdir}/misc/9x18.pcf*
%{_x11fontdir}/misc/9x18B.pcf*
%{_x11fontdir}/misc/k14.pcf*
%{_x11fontdir}/misc/nil2.pcf*
# font-schumacher-misc
%{_x11fontdir}/misc/cl[BIR][456789]x*.pcf*
# encodings
%dir %{_datadir}/fonts/X11/encodings
%dir %{_datadir}/fonts/X11/encodings/large
%{_datadir}/fonts/X11/encodings/*.enc.gz
%ghost %verify(not md5 size mtime) %{_datadir}/fonts/X11/encodings/encodings.dir
%{_datadir}/fonts/X11/encodings/large/*.enc.gz
%ghost %verify(not md5 size mtime) %{_datadir}/fonts/X11/encodings/large/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.cache-*

%files misc
%defattr(-,root,root,-)
%doc
%dir %{_x11fontdir}
%dir %{_x11fontdir}/misc
# font-isas-misc	(Chinese)
%{_x11fontdir}/misc/gb[12][46][fs][st].pcf*
# font-jis-misc		(Japanese)
%{_x11fontdir}/misc/jiskan??.pcf*
# font-mutt-misc
%{_x11fontdir}/misc/cu-alt12.pcf*
%{_x11fontdir}/misc/cu-arabic12.pcf*
%{_x11fontdir}/misc/cu-devnag12.pcf*
%{_x11fontdir}/misc/cu-lig12.pcf*
%{_x11fontdir}/misc/cu-pua12.pcf*
%{_x11fontdir}/misc/cu12.pcf*
%{_x11fontdir}/misc/cuarabic12.pcf*
%{_x11fontdir}/misc/cudevnag12.pcf*
# font-micro-misc
%{_x11fontdir}/misc/micro.pcf*
# font-sony-misc	(Japanese and ISO-8859-1)
%{_x11fontdir}/misc/12x24.pcf*
%{_x11fontdir}/misc/12x24rk.pcf*
%{_x11fontdir}/misc/8x16.pcf*
%{_x11fontdir}/misc/8x16rk.pcf*
# font-sun-misc		(OpenLook glyphs)
%{_x11fontdir}/misc/olcursor.pcf*
%{_x11fontdir}/misc/olgl1?.pcf*
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/encodings.dir
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.dir
# NOTE: Xorg supplies this fonts.alias, so it is not ghosted
%verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.alias
%ghost %verify(not md5 size mtime) %{_x11fontdir}/misc/fonts.cache-*


%changelog
* Fri Oct 23 2015 cjacker - 7.5-4
- Rebuild for new 4.0 release

