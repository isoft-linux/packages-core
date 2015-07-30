Summary: The basic directory layout for a Linux system.
Name: filesystem
Version: 6.8 
Release: 2 
License: Public Domain
Group:  Core/Runtime/Data
Buildroot: %{_tmppath}/%{name}-%{version}-root
Requires(pre): setup >= 2.5.4-1

%description
The filesystem package is one of the basic packages that is installed
on a Red Hat Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories.

%prep

%install
rm -rf %{buildroot}
mkdir %{buildroot}

cd %{buildroot}

mkdir -p mnt/{floppy,cdrom} \
	   boot \
    run/lock \
	etc/{X11/{applnk,sysconfig,serverconfig,starthere},opt,xinetd.d,skel,sysconfig,pki} \
	home usr/lib/modules usr/lib/tls media mnt opt proc root srv sys tmp \
        usr/{bin,etc,include,lib/{gcc-lib,tls,X11},lib,libexec,local/{bin,etc,lib,sbin,src,share/{man/man{1,2,3,4,5,6,7,8,9,n},info},libexec,include,},sbin,share/{applications,doc,dict,info,man/man{1,2,3,4,5,6,7,8,9,n},doc,misc,empty,pixmaps,xsessions},src} \
        var/{empty,lib/misc,local,lock/subsys,log,nis,preserve,run,spool/{mail,lpd},tmp,db,cache,opt,yp}

ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail
ln -sf usr/lib lib
ln -sf usr/bin bin
ln -sf usr/sbin sbin
ln -sf usr/lib lib64
pushd usr
ln -sf lib lib64
popd

%clean
#rm -rf %{buildroot}

%post -p <lua>
posix.symlink("../run", "/var/run")
posix.symlink("../run/lock", "/var/lock")


%files
%defattr(0755,root,root)
%dir /
/bin
/boot
/etc
/home
/lib
/lib64
/media
%dir /mnt
%ghost %config(missingok) %verify(not size md5 mode user link rdev group mtime) /mnt/cdrom
%ghost %config(missingok) %verify(not size md5 mode user link rdev group mtime) /mnt/floppy
%dir /opt
%attr(555,root,root) /proc
%attr(555,root,root) /sys
%attr(750,root,root) /root
%attr(555,root,root) /sbin
/srv
/run
%attr(1777,root,root) /tmp
%dir /usr
/usr/[^s]*
/usr/sbin
%dir /usr/share
/usr/share/applications
/usr/share/doc
/usr/share/dict
%attr(555,root,root) %dir /usr/share/empty
/usr/share/info
/usr/share/man
/usr/share/misc
/usr/share/pixmaps
/usr/share/xsessions
/usr/src
%dir /var
/var/db
/var/lib
/var/local
/var/cache
/var/empty
/var/log
/var/mail
/var/nis
/var/opt
/var/preserve
%ghost %dir %attr(755,root,root) /var/lock
%ghost /var/lock/subsys
%ghost %attr(755,root,root) /var/run

%dir /var/spool
%attr(755,root,root) /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(1777,root,root) /var/tmp
/var/yp

