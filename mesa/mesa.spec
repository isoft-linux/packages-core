%define with_opencl 1

Summary: Mesa graphics libraries
Name: mesa
Version: 10.7.0
Release: 5.git 
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
#Source0: mesa-%{version}.tar.xz
#20150710
#git clone git://anongit.freedesktop.org/mesa/mesa
Source0:    mesa.tar.gz

#this patch used to build mesa with llvm/libcxx
#currently not applied, just keep it here.
#By Cjacker.
Patch0: mesa-fix-build-with-llvm-libc++.patch

# https://bugs.freedesktop.org/show_bug.cgi?id=73512
Patch10: 0001-opencl-use-versioned-.so-in-mesa.icd.patch

#from mesa-10.4, intel dri had a critical crash problem 
#and up to now, it's still not fixed.
#this is a try to avoid irb->mt is null.
#By Cjacker.
Patch20: mesa-try-fix-intel-brw_meta_fast_clear-crash.patch
#not sure, try to use plain_clear.
Patch21: mesa-try-fix-intel-brw_meta_fast_clear-crash-use-PLAIN_CLEAR.patch


BuildRequires: pkgconfig autoconf automake
BuildRequires: libdrm-devel >= 2.4.18-0.1
BuildRequires: expat-devel >= 2.0
BuildRequires: python
BuildRequires: wayland-devel
BuildRequires: libllvm-devel
#it need libLLVM shared library
BuildRequires: libllvm
BuildRequires: xorg-x11-proto-devel >= 7.4-35
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libvdpau-devel
BuildRequires: libva-devel
BuildRequires: libxshmfence-devel
BuildRequires: libXvMC-devel

%if 0%{?with_opencl}
BuildRequires: libclang-devel >= 3.0
BuildRequires: libclc-devel libllvm-static
%endif


%description
Mesa graphics libraries

%package libGL
Summary: Mesa libGL runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGL
Requires: mesa-dri-drivers = %{version}-%{release}
Requires: libdrm >= 2.4.18-0.1

%description libGL
Mesa libGL runtime library.

%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Provides: libGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libGL-devel
Mesa libGL development package

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libEGL
Requires: mesa-dri-drivers = %{version}-%{release}
Requires: libdrm >= 2.4.18-0.1

%description libEGL
Mesa libEGL runtime library.


%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
%description dri-drivers
Mesa-based DRI drivers.


%package libEGL-devel
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}
Provides: libEGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libEGL-devel
Mesa libEGL development package


%package libgbm
Summary: Mesa gbm library
Group: System Environment/Libraries
Provides: libgbm

%description libgbm
Mesa gbm runtime library.


%package libgbm-devel
Summary: Mesa libgbm development package
Group: Development/Libraries
Requires: mesa-libgbm = %{version}-%{release}
Provides: libgbm-devel

%description libgbm-devel
Mesa libgbm development package

%package libwayland-egl
Summary: Mesa libwayland-egl library
Group: System Environment/Libraries
Provides: libwayland-egl

%description libwayland-egl
Mesa libwayland-egl runtime library.


%package libwayland-egl-devel
Summary: Mesa libwayland-egl development package
Group: Development/Libraries
Requires: mesa-libwayland-egl = %{version}-%{release}
Provides: libwayland-egl-devel

%description libwayland-egl-devel
Mesa libwayland-egl development package


%package libGLESv2
Summary: Mesa libGLESv2 runtime libraries
Group: System Environment/Libraries
Provides: mesa-libGLES = %{version}-%{release}

%description libGLESv2
Mesa GLESv2 runtime libraries

%package libGLESv2-devel
Summary: Mesa libGLESv2 development package
Group: Development/Libraries
Requires: mesa-libGLESv2 = %{version}-%{release}
Provides: mesa-libGLES-devel = %{version}-%{release}

%description libGLESv2-devel
Mesa libGLESv2 development package


%package libxatracker
Summary: Xorg Gallium3D acceleration library 
Group: System Environment/Libraries

%description libxatracker
Xorg Gallium3D acceleration library

%package libxatracker-devel
Summary: Mesa libxatracker development package
Group: Development/Libraries
Requires: mesa-libxatracker = %{version}-%{release}

%description libxatracker-devel
Development libraries and headers for Xorg Gallium3D acceleration library

%package libXvmc
Summary: Mesa libXvmc runtime libraries
Group: System Environment/Libraries

%description libXvmc
Mesa Xvmc runtime libraries

%package libvdpau-plugins
Summary: Mesa plugins for libvdpau.
Group: System Environment/Libraries
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
Group: System Environment/Libraries
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
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

%if 0%{?with_opencl}
%patch10 -p1 -b .icd
%endif

%patch20 -p1
#%patch21 -p1

%build
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
  --with-egl-platforms=x11,wayland,drm \
  --enable-shared-glapi \
  --enable-xvmc \
  --enable-vdpau \
  --enable-va \
  --enable-glx-tls \
  --enable-gallium-llvm \
  --enable-llvm-shared-libs \
  --enable-gallium-egl \
  --with-gallium-drivers="i915,nouveau,svga,r300,r600,radeonsi,swrast" \
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

%if 0%{?with_opencl}
%post libOpenCL -p /sbin/ldconfig
%postun libOpenCL -p /sbin/ldconfig
%endif


%files libGL
%{_libdir}/libGL.so.*

%files libGL-devel
%{_libdir}/libGL.so
%{_includedir}/GL/glx*.h

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
%{_libdir}/libglapi*.so.*
%{_libdir}/libEGL*.so.*


%files libEGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glcorearb.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_includedir}/GL/osmesa.h

%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/libglapi*.so
%{_libdir}/libEGL*.so

%files dri-drivers
%defattr(-,root,root,-)
%config %{_sysconfdir}/drirc
%dir %{_libdir}/dri
%{_libdir}/dri/*_dri.so
%{_libdir}/dri/gallium_drv_video.so
#%{_libdir}/egl/egl_gallium.so
#%{_libdir}/gbm/gbm_gallium_drm.so
%{_libdir}/gallium-pipe/pipe_*.so

%files libwayland-egl
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*

%files libwayland-egl-devel
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc


%files libGLESv2
%defattr(-,root,root,-)
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*


%files libGLESv2-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv2.so
%{_includedir}/GLES3

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
%doc docs/COPYING
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

