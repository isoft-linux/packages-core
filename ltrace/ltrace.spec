Summary: Tracks runtime library calls from dynamically linked executables
Name: ltrace
Version: 0.7.91
Release: 18%{?dist}
URL: http://ltrace.alioth.debian.org/
License: GPLv2+

BuildRequires: libelfutils-devel dejagnu
BuildRequires: autoconf automake libtool

# Note: this URL needs to be updated for each release, as the file
# number changes for each file.  Full list of released files is at:
#  https://alioth.debian.org/frs/?group_id=30892
Source: ltrace-%{version}.tar.bz2

# Merge of several upstream commits that fixes compilation on ARM.
Patch0: ltrace-0.7.91-arm.patch

# Upstream patch that fixes accounting of exec, __libc_start_main and
# others in -c output.
Patch1: ltrace-0.7.91-account_execl.patch

# Upstream patch that fixes interpretation of PLT on x86_64 when
# IRELATIVE slots are present.
Patch2: ltrace-0.7.91-x86_64-irelative.patch

# Upstream patch that fixes fetching of system call arguments on s390.
Patch3: ltrace-0.7.91-s390-fetch-syscall.patch

# Upstream patch that enables tracing of IRELATIVE PLT slots on s390.
Patch4: ltrace-0.7.91-s390-irelative.patch

# Fix for a regression in tracing across fork.  Upstream patch.
Patch5: ltrace-0.7.91-ppc64-fork.patch

# Fix crashing a prelinked PPC64 binary which makes PLT calls through
# slots that ltrace doesn't trace.
# https://bugzilla.redhat.com/show_bug.cgi?id=1051221
Patch6: ltrace-0.7.91-breakpoint-on_install.patch
Patch7: ltrace-0.7.91-ppc64-unprelink.patch

# Man page nits.  Backport of an upstream patch.
Patch8: ltrace-0.7.91-man.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1044766
Patch9: ltrace-0.7.91-cant_open.patch

# Support Aarch64 architecture.
Patch10: ltrace-0.7.91-aarch64.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1064406
Patch11: ltrace-0.7.2-e_machine.patch

# Support for ppc64le, backported from upstream.
# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=eea4ad2cce289753aaa35b4e0258a76d8f8f367c
# https://bugzilla.redhat.com/show_bug.cgi?id=1131956
Patch13: ltrace-0.7.91-ppc64le-support.patch
# 35a9677dc9dcb7909ebd28f30200474d7e8b660f,
# 437d2377119036346f4dbd93039c847b4cc9d0be,
# eb3993420734f091cde9a6053ca6b4edcf9ae334
Patch14: ltrace-0.7.91-ppc64le-fixes.patch

# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=2e9f9f1f5d0fb223b109429b9c904504b7f638e2
# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=f96635a03b3868057db5c2d7972d5533e2068345
Patch15: ltrace-0.7.91-parser-ws_after_id.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1171165
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=d8f1287b85e2c2b2ae0235809e956f4365e53c45
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=d80c5371454383e3f9978622e5578cf02af8c44c
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=bf82100966deda9c7d26ad085d97c08126a8ae88
Patch16: ltrace-0.7.91-ppc-bias.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1158714
Patch17: ltrace-0.7.91-x86-plt_map.patch
Patch18: ltrace-0.7.91-x86-unused_label.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1170315
Patch19: ltrace-0.7.91-unwind-elfutils.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1208351
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=4724bd5a4a19db117a1d280b9d1a3508fd4e03fa
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=72ee29639c55b5942bc07c8ed0013005f8fc5a97
Patch20: ltrace-0.7.91-multithread-no-f-1.patch
Patch21: ltrace-0.7.91-multithread-no-f-2.patch

# Fix problems with building a number of test cases.
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=694d19ff14017926454771cbb63a22355b72f1bf
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=a3a03622fb4ca9772dca13eae724a94ba1e728f4
Patch22: ltrace-0.7.91-testsuite-includes.patch
Patch23: ltrace-0.7.91-testsuite-includes-2.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1210653
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=eea6091f8672b01f7f022b0fc367e0f568225ffc
Patch24: ltrace-0.7.91-ppc64le-configure.patch

%description
Ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process.  Ltrace can also
intercept and print system calls executed by the process.

You should install ltrace if you need a sysadmin tool for tracking the
execution of processes.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

%build
autoreconf -i
%configure --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} install

# The testsuite is useful for development in real world, but fails in
# koji for some reason.  Disable it, but have it handy.
%check
echo ====================TESTING=========================
timeout 180 make check ||:
echo ====================TESTING END=====================

%files
%defattr(-,root,root)
%doc NEWS
%{_bindir}/ltrace
%{_mandir}/man1/ltrace.1*
%{_mandir}/man5/ltrace.conf.5*
%{_datadir}/ltrace

%changelog
* Fri Oct 30 2015 Cjacker <cjacker@foxmail.com> - 0.7.91-18
- Import from fedora

