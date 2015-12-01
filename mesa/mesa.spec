%define with_opencl 1

Summary: Mesa graphics libraries
Name: mesa
Version: 11.1.0
Release: 62.llvm37.git
License: MIT
URL: http://www.mesa3d.org

#git clone git://anongit.freedesktop.org/mesa/mesa
Source0: mesa-4d64459.tar.xz

#this patch used to build mesa with llvm/libcxx
#currently not applied, just keep it here.
#By Cjacker.
Patch0: mesa-fix-build-with-llvm-libc++.patch

#if build mesa with clang, should apply this patch.
Patch1: mesa-hide-some-symbols-to-workaround-build-with-llvm-clang.patch

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: kernel-headers
BuildRequires: xorg-x11-server-devel

BuildRequires: libdrm-devel >= 2.4.42
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: libxshmfence-devel
BuildRequires: libX11-devel
BuildRequires: libXv-devel
BuildRequires: libXvMC-devel
BuildRequires: libXxf86vm-devel

BuildRequires: elfutils
BuildRequires: python
BuildRequires: gettext
BuildRequires: libelfutils-devel
BuildRequires: python-libxml2
#for libudev
BuildRequires: systemd-devel 
BuildRequires: bison flex
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: libvdpau-devel
BuildRequires: zlib-devel
BuildRequires: wayland-devel
BuildRequires: libllvm-devel
BuildRequires: libclang-devel
#it need libLLVM shared library
BuildRequires: libllvm
#it need clang internal header
BuildRequires: clang
BuildRequires: libva-devel
BuildRequires: libXvMC-devel
BuildRequires: python-mako

BuildRequires: libxcb-devel

BuildRequires: nettle-devel

%if 0%{?with_opencl}
BuildRequires: libclang-devel >= 3.0
BuildRequires: libclc-devel libllvm-static libclang-static
%endif


%description
Mesa graphics libraries

%package libGL
Summary: Mesa libGL runtime libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGL
Provides: libglapi
Provides: mesa-libglapi
Requires: mesa-dri-drivers = %{version}-%{release}
Requires: libdrm >= 2.4.18-0.1

%description libGL
Mesa libGL runtime library.

%package libGL-devel
Summary: Mesa libGL development package
Requires: mesa-libGL = %{version}-%{release}
Provides: libGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libGL-devel
Mesa libGL development package

%package libEGL
Summary: Mesa libEGL runtime libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libEGL
Requires: mesa-dri-drivers = %{version}-%{release}
Requires: libdrm >= 2.4.18-0.1

%description libEGL
Mesa libEGL runtime library.


%package dri-drivers
Summary: Mesa-based DRI drivers
%description dri-drivers
Mesa-based DRI drivers.


%package libEGL-devel
Summary: Mesa libEGL development package
Requires: mesa-libEGL = %{version}-%{release}
Provides: libEGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libEGL-devel
Mesa libEGL development package


%package libgbm
Summary: Mesa gbm library
Provides: libgbm

%description libgbm
Mesa gbm runtime library.


%package libgbm-devel
Summary: Mesa libgbm development package
Requires: mesa-libgbm = %{version}-%{release}
Provides: libgbm-devel

%description libgbm-devel
Mesa libgbm development package

%package libwayland-egl
Summary: Mesa libwayland-egl library
Provides: libwayland-egl

%description libwayland-egl
Mesa libwayland-egl runtime library.


%package libwayland-egl-devel
Summary: Mesa libwayland-egl development package
Requires: mesa-libwayland-egl = %{version}-%{release}
Provides: libwayland-egl-devel

%description libwayland-egl-devel
Mesa libwayland-egl development package


%package libGLES
Summary: Mesa libGLES runtime libraries
Provides: mesa-libGLESv2 = %{version}-%{release}

%description libGLES
Mesa GLESv2 runtime libraries

%package libGLES-devel
Summary: Mesa libGLES development package
Requires: mesa-libGLES = %{version}-%{release}
Provides: mesa-libGLESv2-devel = %{version}-%{release}

%description libGLES-devel
Mesa libGLES development package


%package libxatracker
Summary: Xorg Gallium3D acceleration library 

%description libxatracker
Xorg Gallium3D acceleration library

%package libxatracker-devel
Summary: Mesa libxatracker development package
Requires: mesa-libxatracker = %{version}-%{release}

%description libxatracker-devel
Development libraries and headers for Xorg Gallium3D acceleration library

%package libXvmc
Summary: Mesa libXvmc runtime libraries

%description libXvmc
Mesa Xvmc runtime libraries

%package libvdpau-plugins
Summary: Mesa plugins for libvdpau.
Requires: libvdpau

%description libvdpau-plugins 
Mesa plugins for libvdpau.

%package libd3d
Summary: Mesa Direct3D9 state tracker

%description libd3d
Mesa Direct3D9 state tracker

%package libd3d-devel
Summary: Mesa Direct3D9 state tracker development package
Requires: mesa-libd3d%{?_isa} = %{version}-%{release}

%description libd3d-devel
Mesa Direct3D9 state tracker development package


%package libOSMesa
Summary: Mesa offscreen rendering libraries
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package


%if 0%{?with_opencl}
%package libOpenCL
Summary: Mesa OpenCL runtime library
Requires: ocl-icd
Requires: libclc
Requires: mesa-libgbm = %{version}-%{release}

%description libOpenCL
Mesa OpenCL runtime library.

%package libOpenCL-devel
Summary: Mesa OpenCL development package
Requires: mesa-libOpenCL%{?_isa} = %{version}-%{release}

%description libOpenCL-devel
Mesa OpenCL development package.
%endif


%prep
%setup -q -n %{name} 

%build
#make sure mesa build with gcc/g++
export CC=gcc
export CXX=g++

export CFLAGS="$RPM_OPT_FLAGS"
#we had to force -fno-rtti -fno-exceptions here.
#But it will failed clover build.
#Remove this flags when configure done for clover.
#export CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions"
#for opencl, dependen on LLVM build configuration.
export CXXFLAGS="$RPM_OPT_FLAGS -frtti -fexceptions"

./autogen.sh --disable-glx --with-egl-platforms=wayland,drm

%configure \
%ifarch %{ix86}
     --disable-asm
%endif
  %{?with_opencl:--enable-opencl --enable-opencl-icd --with-clang-libdir=%{_prefix}/lib} %{!?with_opencl:--disable-opencl} \
  --enable-dri \
  --enable-osmesa \
  --enable-glx \
  --with-egl-platforms=x11,wayland,drm,surfaceless \
  --enable-shared-glapi \
  --enable-xvmc \
  --enable-vdpau \
  --enable-va \
  --enable-glx-tls \
  --enable-gallium-llvm \
  --enable-llvm-shared-libs \
  --enable-gallium-egl \
  --with-gallium-drivers="i915,ilo,nouveau,svga,r300,r600,radeonsi,swrast,virgl" \
  --with-dri-drivers="swrast,nouveau,radeon,r200,i915,i965" \
  --enable-egl \
  --enable-gles2 \
  --disable-gles1 \
  --enable-texture-float \
  --enable-gbm \
  --enable-nine \
  --enable-xa 

#fix clover build
#sed -i 's/-fno-rtti -fno-exceptions//g'  src/gallium/state_trackers/clover/Makefile

make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT

# core libs and headers, but not drivers.
make install DESTDIR=$RPM_BUILD_ROOT

# strip out undesirable headers
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/w*.h

# remove .la files
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd $RPM_BUILD_ROOT%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig

%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig

%post libd3d -p /sbin/ldconfig
%postun libd3d -p /sbin/ldconfig

%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig

%post libGLES -p /sbin/ldconfig
%postun libGLES -p /sbin/ldconfig

%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig

%post libwayland-egl -p /sbin/ldconfig
%postun libwayland-egl -p /sbin/ldconfig

%post libxatracker -p /sbin/ldconfig
%postun libxatracker -p /sbin/ldconfig

%if 0%{?with_opencl}
%post libOpenCL -p /sbin/ldconfig
%postun libOpenCL -p /sbin/ldconfig
%endif


%files libGL
%{_libdir}/libGL.so.*
%{_libdir}/libglapi*.so.*

%files libGL-devel
%{_libdir}/libGL.so
%{_libdir}/libglapi*.so
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glcorearb.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/pkgconfig/gl.pc

%files libXvmc
%defattr(-,root,root,-)
%{_libdir}/libXvMCnouveau.so
%{_libdir}/libXvMCnouveau.so.*
%{_libdir}/libXvMCr600.so
%{_libdir}/libXvMCr600.so.*

%files libvdpau-plugins
%defattr(-,root,root,-)
%{_libdir}/vdpau/*

%files libEGL
%defattr(-,root,root,-)
%{_libdir}/libEGL*.so.*


%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglextchromium.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files dri-drivers
%defattr(-,root,root,-)
%config %{_sysconfdir}/drirc
%dir %{_libdir}/dri
%{_libdir}/dri/*_dri.so
%{_libdir}/dri/gallium_drv_video.so
%{_libdir}/gallium-pipe/pipe_*.so

%files libwayland-egl
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*

%files libwayland-egl-devel
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc


%files libGLES
%defattr(-,root,root,-)
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*


%files libGLES-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%dir %{_includedir}/GLES3
%{_includedir}/GLES3/gl3platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl3ext.h
%{_includedir}/GLES3/gl31.h
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv2.so

%files libxatracker
%defattr(-,root,root,-)
%{_libdir}/libxatracker.so.*

%files libxatracker-devel
%defattr(-,root,root,-)
%{_libdir}/libxatracker.so
%{_libdir}/pkgconfig/xatracker.pc
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_includedir}/xa_tracker.h

%files libgbm
%defattr(-,root,root,-)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root,-)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%files libOSMesa
%defattr(-,root,root,-)
%{_libdir}/libOSMesa.so.8*

%files libOSMesa-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files libd3d
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*

%files libd3d-devel
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif


%changelog
* Tue Dec 01 2015 sulit - 11.1.0-62.llvm37.git
- update to git 4d64459, 11.1.0-rc2 comes
- include various updates to i965 and various fixes to r600

* Thu Nov 26 2015 sulit <sulitsrc@gmail.com> - 11.1.0-61.llvm37.git
- update to git 63c344d, include various fixes to i965/radeon,
- add some support, I clean sources file

* Mon Nov 23 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-60.llvm37.git
- Update

* Fri Nov 20 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-59.llvm37.git
- Update

* Thu Nov 19 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-58.llvm37.git
- Update, include various fixes to i965/radeon

* Wed Nov 18 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-57.llvm37.git
- Update to git 27b1d34, with dri3 and intel improvement

* Tue Nov 17 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-56.llvm37.git
- Update to latest git, include fixes for ati/intel

* Mon Nov 16 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-55.llvm37.git
- Update

* Thu Nov 12 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-54.llvm37.git
- Update to git 55314c5

* Wed Nov 11 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-53.llvm37.git
- Update to git 3f45d29

* Sun Nov 08 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-52.llvm37.git
- Update to df4f9b0

* Sat Nov 07 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-51.llvm37.git
- Update to mesa-8e9ade7

* Thu Nov 05 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-50.llvm37.git
- Update to latest git, Intel  ARB_arrays_of_arrays  support included

* Wed Nov 04 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-49.llvm37.git
- Update to git 4bc16ad, We will update mesa codes Util mesa 11.1 released

* Sun Nov 01 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-48.llvm37.git
- Update to git 39bb59a

* Sat Oct 31 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-47.llvm37.git
- git 103de02

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-46.llvm37.git
- Update to git 7b8cc37

* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-45.llvm37.git
- Add more build requires

* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-44.llvm37.git
- Update, enable virgl

* Thu Oct 29 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-43.llvm37.git
- Update to git 85f1f044

* Mon Oct 26 2015 Cjacker <cjacker@foxmail.com> - 11.1.0-42.git
- Update to 3359ad6 git.

* Fri Oct 23 2015 cjacker - 11.1.0-40.git
- Rebuild for new 4.0 release

* Mon Aug 24 2015 Cjacker <cjacker@foxmail.com>
- update to laste git codes.
- revert radeon IB buffer size for better performance and other regular commits.

* Fri Aug 14 2015 Cjacker <cjacker@foxmail.com>
- update, amdgpu enter mainline

* Wed Aug 12 2015 Cjacker <cjacker@foxmail.com>
- update to 02a4fe2
- add patch10 to fix intel crash bug.

* Tue Aug 11 2015 Cjacker <cjacker@foxmail.com>
- update to 87cea61

* Sat Aug 08 2015 Cjacker <cjacker@foxmail.com>
- update to a1adf0b

* Fri Aug 07 2015 Cjacker <cjacker@foxmail.com>
- update to 42d283a

* Wed Aug 05 2015 Cjacker <cjacker@foxmail.com>
- update to 03b7221
- remove patch20

* Tue Aug 04 2015 Cjacker <cjacker@foxmail.com>
- update to 996349c

* Thu Jul 30 2015 Cjacker <cjacker@foxmail.com>
- update to c73a13e

* Wed Jul 29 2015 Cjacker <cjacker@foxmail.com>
- update to 2e04492

* Sun Jul 26 2015 Cjacker <cjacker@foxmail.com>
- update to bb9d59a

* Sat Jul 25 2015 Cjacker <cjacker@foxmail.com>
- update to 7b40d92

* Fri Jul 24 2015 Cjacker <cjacker@foxmail.com>
- update to git 30f97b5

* Thu Jul 23 2015 Cjacker <cjacker@foxmail.com>
- update to git c6267eb

* Thu Jul 23 2015 Cjacker <cjacker@foxmail.com>
- update to git 6d8e466

* Wed Jul 22 2015 Cjacker <cjacker@foxmail.com>
- update to git 13322a6
- add OpenGL 4.x GL_ARB_get_texture_sub_image extension.

* Tue Jul 21 2015 Cjacker <cjacker@foxmail.com>
- update to git b298311

* Sun Jul 19 2015 Cjacker <cjacker@foxmail.com>
- update to git 8c8a71f

* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- update to git head 01cdbba

* Thu Jul 16 2015 Cjacker <cjacker@foxmail.com>
- update to git head 779cabf
- by the way, irb->mt crash issue seems disappear.

* Wed Jul 15 2015 Cjacker <cjacker@foxmail.com>
- Add patch #20, #21, try to fix i965 irb->mt segfault issue.
 
* Tue Dec 10 2013 Cjacker <cjacker@gmail.com>
- first build, prepare for the new release.

