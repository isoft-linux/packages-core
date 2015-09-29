Summary:    The GNU shar utilities for packaging and unpackaging shell archives
Name:       sharutils
Version:    4.15.2
Release:    2%{?dist}
# The main code:                GPLv3+
# lib (gnulib):                 GPLv3+
# lib/md5.c:                    Public Domain
# libopts:                      LGPLv3+ or BSD
# libopts/genshell.h            LGPLv2+
# libopts/m4/libopts.m4:        GPLv3+
# doc/sharutils.texi:           GFDL
License:    GPLv3+ and (LGPLv3+ or BSD) and LGPLv2+ and Public Domain and GFDL
Group:      Applications/Archiving
Source:     ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
# Pass compilation with -Werror=format-security, bug #1037323
Patch0:     %{name}-4.14.2-Pass-compilation-with-Werror-format-security.patch
URL:        http://www.gnu.org/software/%{name}/
BuildRequires:      binutils
BuildRequires:      coreutils
BuildRequires:      gcc
BuildRequires:      gettext
BuildRequires:      glibc-common
BuildRequires:      glibc-headers
BuildRequires:      make
BuildRequires:      sed
# Tests:
BuildRequires:      diffutils
#Requires(post):     info
#Requires(preun):    info
Provides:           bundled(gnulib)
# See libopts/autoopts/options.h for OPTIONS_DOTTED_VERSION
Provides:           bundled(libopts) = 41.1

%description
The sharutils package contains the GNU shar utilities, a set of tools for
encoding and decoding packages of files (in binary or text format) in
a special plain text format called shell archives (shar).  This format can be
sent through e-mail (which can be problematic for regular binary files).  The
shar utility supports a wide range of capabilities (compressing, uuencoding,
splitting long files for multi-part mailings, providing check-sums), which
make it very flexible at creating shar files.  After the files have been sent,
the unshar tool scans mail messages looking for shar files.  Unshar
automatically strips off mail headers and introductory text and then unpacks
the shar files.

%prep
%setup -q
%patch0 -p1 -b .format

# convert TODO, THANKS to UTF-8
for i in TODO THANKS; do
  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
  mv $i{.utf8,}
done

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
chmod 644 AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%find_lang %{name}

%check
make check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_infodir}/*info*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
