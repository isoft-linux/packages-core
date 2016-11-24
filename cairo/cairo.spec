%define pixman_version 0.32.6
%define freetype_version 2.1.9
%define fontconfig_version 2.2.95

Summary: A 2D graphics library
Name:  cairo
Version: 1.14.6
Release: 3
URL:  http://cairographics.org
License: LGPLv2 or MPLv1.1

Source0: %{name}-%{version}.tar.xz
Patch0: cairo-make-lcdfilter-default.patch
Patch1: cairo-respect-fontconfig_pb.patch
Patch2: cairo-server-side-gradients.patch
Patch3: cairo-webkit-html5-fix.patch
Patch4: cairo-color-glyphs.patch

BuildRequires: pkgconfig
BuildRequires: libXrender-devel
BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: glib2-devel
#BuildRequires: librsvg2-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel

%description
Cairo is a 2D graphics library designed to provide high-quality display
and print output. Currently supported output targets include the X Window
System, OpenGL (via glitz), in-memory image buffers, and image files (PDF,
PostScript, and SVG).

Cairo is designed to produce consistent output on all output media while
taking advantage of display hardware acceleration when available (e.g.
through the X Render Extension or OpenGL).

%package devel
Summary: Development files for cairo
Requires: %{name} = %{version}-%{release}
Requires: libpng-devel
Requires: pixman-devel >= %{pixman_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}

%description devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo graphics library.

%package gobject
Summary: GObject bindings for cairo
Requires: %{name} = %{version}-%{release}

%description gobject
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains functionality to make cairo graphics library
integrate well with the GObject object system used by GNOME.

%package gobject-devel
Summary: Development files for cairo-gobject
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-gobject = %{version}-%{release}

%description gobject-devel
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains libraries, header files and developer documentation
needed for developing software which uses the cairo Gobject library.

%package tools
Summary: Development tools for cairo

%description tools
Cairo is a 2D graphics library designed to provide high-quality display
and print output.

This package contains tools for working with the cairo graphics library.
 * cairo-trace: Record cairo library calls for later playback

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %configure --disable-static \
    --enable-xlib \
    --enable-ft \
    --enable-ps \
    --enable-pdf \
    --enable-svg \
    --enable-tee \
    --enable-gobject \
    --enable-gl \
    --disable-gtk-doc \
    --disable-gtk-doc-html

#add -rtlib=compiler-rt to fix cairo build with clang, without gcc, some symbol will missing.
#it cause a symbol leak of dynamic library of cairo.
#sed -i "s@pic_flag=\" -fPIC -DPIC\"@pic_flag=\" -rtlib=compiler-rt -fPIC -DPIC\"@g" libtool

#Hmm..., O0 for clang, O1/O2 will cause a very strange segfault(when toggle inputmethod pgup/pgdown)
#sed -i "s@-O2@-O0@g" src/Makefile

make %{?_smp_mflags}

%install
make install V=1 DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gobject -p /sbin/ldconfig
%postun gobject -p /sbin/ldconfig

%files
%{_libdir}/libcairo.so.*
%{_libdir}/libcairo-script-interpreter.so.*
%{_bindir}/cairo-sphinx

%files devel
%dir %{_includedir}/cairo/
%{_includedir}/cairo/cairo-deprecated.h
%{_includedir}/cairo/cairo-features.h
%{_includedir}/cairo/cairo-ft.h
%{_includedir}/cairo/cairo.h
%{_includedir}/cairo/cairo-pdf.h
%{_includedir}/cairo/cairo-ps.h
%{_includedir}/cairo/cairo-script-interpreter.h
%{_includedir}/cairo/cairo-svg.h
%{_includedir}/cairo/cairo-tee.h
%{_includedir}/cairo/cairo-version.h
%{_includedir}/cairo/cairo-gl.h
%{_includedir}/cairo/cairo-script.h
%{_libdir}/libcairo.so
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/pkgconfig/cairo-fc.pc
%{_libdir}/pkgconfig/cairo-ft.pc
%{_libdir}/pkgconfig/cairo.pc
%{_libdir}/pkgconfig/cairo-pdf.pc
%{_libdir}/pkgconfig/cairo-png.pc
%{_libdir}/pkgconfig/cairo-ps.pc
%{_libdir}/pkgconfig/cairo-svg.pc
%{_libdir}/pkgconfig/cairo-tee.pc
%{_libdir}/pkgconfig/cairo-egl.pc
%{_libdir}/pkgconfig/cairo-script.pc

%{_includedir}/cairo/cairo-xcb.h
%{_includedir}/cairo/cairo-xlib-xrender.h
%{_includedir}/cairo/cairo-xlib.h
%{_libdir}/pkgconfig/cairo-xcb-shm.pc
%{_libdir}/pkgconfig/cairo-xcb.pc
#%{_libdir}/pkgconfig/cairo-xlib-xcb.pc
%{_libdir}/pkgconfig/cairo-xlib-xrender.pc
%{_libdir}/pkgconfig/cairo-xlib.pc
%{_libdir}/pkgconfig/cairo-gl.pc
%{_libdir}/pkgconfig/cairo-glx.pc

%{_datadir}/gtk-doc/html/cairo

%files gobject
%{_libdir}/libcairo-gobject.so.*

%files gobject-devel
%{_includedir}/cairo/cairo-gobject.h
%{_libdir}/libcairo-gobject.so
%{_libdir}/pkgconfig/cairo-gobject.pc

%files tools
%{_bindir}/cairo-trace
%{_libdir}/cairo/

%changelog
* Thu Nov 24 2016 sulit <sulitsrc@163.com> - 1.14.6-3
- rebuild

* Tue Nov 22 2016 cjacker - 1.14.6-2
- Update to 1.14.6

* Fri Oct 23 2015 cjacker - 1.14.2-4
- Rebuild for new 4.0 release

* Mon Oct 12 2015 Cjacker <cjacker@foxmail.com>
- rebuild, change configure options.
