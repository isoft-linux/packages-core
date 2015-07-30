Name:	    tzdata	
Version:	2015e
Release:	1
Summary:	Time Zone Database

Group:		Core/Runtime/Data
License:	Public Domain
URL:		http://www.iana.org/time-zones
Source0:	tzdata%{version}.tar.gz
Source1:    tzcode%{version}.tar.gz
Source2:    http://dev.alpinelinux.org/archive/posixtz/posixtz-0.3.tar.bz2
Patch0:     tzdata-makefile.patch 
Patch1:     0001-posixtz-fix-up-lseek.patch

%description
The Time Zone Database (often called tz or zoneinfo) contains code and data that represent the history of local time for many representative locations around the globe. It is updated periodically to reflect changes made by political bodies to time zone boundaries, UTC offsets, and daylight-saving rules. Its management procedure is documented in BCP 175: Procedures for Maintaining the Time Zone Database.

%prep
%setup -q -c -a1 -a2
%patch0 -p1
%patch1 -p1


%build
export CC=gcc

make CFLAGS="$CFLAGS -DHAVE_STDINT_H=1"
pushd posixtz-0.3
make posixtz
popd


%install
make install DESTDIR=%{buildroot}
install -m0755 posixtz-0.3/posixtz $RPM_BUILD_ROOT%{_bindir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
rm -rf $RPM_BUILD_ROOT%{_bindir}/tzselect

%files
%{_bindir}/posixtz
%{_libdir}/libtz.a
%{_mandir}/man3/newctime.3.gz
%{_mandir}/man3/newtzset.3.gz
%{_mandir}/man5/tzfile.5.gz
%{_mandir}/man8/tzselect.8.gz
%{_mandir}/man8/zdump.8.gz
%{_mandir}/man8/zic.8.gz
%dir %{_datadir}/zoneinfo
%{_datadir}/zoneinfo/*
