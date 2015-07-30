Summary: A dictionary of English words for the /usr/share/dict directory
Name: words
Version: 3.0
Release: 24%{?dist}
License: Public Domain
Group: System Environment/Libraries
# Note that Moby Project officially does not exist any more. The most complete
# information about the project is in Wikipedia.
URL: http://en.wikipedia.org/wiki/Moby_Project
Source: http://web.archive.org/web/20060527013227/http://www.dcs.shef.ac.uk/research/ilash/Moby/mwords.tar.Z

BuildArch: noarch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dos2unix
BuildRequires: grep

#428582 - linux.words contains misspelled word "flourescent"
#440146 - misspelled word in /usr/share/dict/words (architecure)
#457309 - contains both 'unnecessary' and 'unneccesary'
Patch0: words-3.0-typos.patch
#470921 -"Barack" and "Obama" are not in /usr/share/dict/words
Patch1: words-3.0-presidents.patch

%description
The words file is a dictionary of English words for the
/usr/share/dict directory. Some programs use this database of
words to check spelling. Password checkers use it to look for bad
passwords.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

%build
cd mwords
dos2unix -o *; chmod a+r *
cat [1-9]*.??? | egrep --invert-match "'s$" | egrep  "^[[:alnum:]'&!,./-]+$" | sort --ignore-case --dictionary-order | uniq > moby

cat <<EOF >license.txt
***
    The license in the readme.txt file is original and DEPRECATED
    license of The Moby lexicon project.
***

On June 1, 1996 Grady Ward announced that the fruits of
the Moby project were being placed in the public domain:

The Moby lexicon project is complete and has
been place into the public domain. Use, sell,
rework, excerpt and use in any way on any platform.

Placing this material on internal or public servers is
also encouraged. The compiler is not aware of any
export restrictions so freely distribute world-wide.

You can verify the public domain status by contacting

Grady Ward
3449 Martha Ct.
Arcata, CA  95521-4884

daedal@myrealbox.com
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/dict
install -m644 mwords/moby $RPM_BUILD_ROOT%{_datadir}/dict/linux.words
ln -sf linux.words $RPM_BUILD_ROOT%{_datadir}/dict/words

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc mwords/readme.txt mwords/license.txt
%{_datadir}/dict/linux.words
%{_datadir}/dict/words

%changelog
* Fri Jul 17 2015 Cjacker <cjacker@foxmail.com>
- first build
