Name:		compiler-wrapper
Version:	1.0
Release:	1
Summary:	Compiler Wrapper Scripts to between gcc and clang

Group:	    Core/Development/Utility
License:	BSD

#default clang wrapper to disable libgcc/libstdc++
Source0:    cc.clang-nogcc
Source1:    c++.clang-nogcc

#clang wrapper to disable libgcc/libstdc++ and enable compiler-rt
Source2:    cc.clang-nogcc-with-compiler-rt
Source3:    c++.clang-nogcc-with-compiler-rt

Requires(post): alternatives

%description
Compiler Wrapper Scripts to toggle between gcc and clang.

%prep

%build
%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf gcc cc.gcc
ln -sf g++ c++.gcc
ln -sf clang cc.clang
ln -sf clang++ c++.clang
popd

install -m0755 %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/


%post
rm -f %{_bindir}/cc
rm -f %{_bindir}/c++
%{_sbindir}/alternatives --install %{_bindir}/cc cc \
  %{_bindir}/cc.clang-nogcc 30
%{_sbindir}/alternatives --install %{_bindir}/c++ c++ \
  %{_bindir}/c++.clang-nogcc 30

%{_sbindir}/alternatives --install %{_bindir}/cc cc \
  %{_bindir}/cc.clang-nogcc-with-compiler-rt 30
%{_sbindir}/alternatives --install %{_bindir}/c++ c++ \
  %{_bindir}/c++.clang-nogcc-with-compiler-rt 30

%{_sbindir}/alternatives --install %{_bindir}/cc cc \
  %{_bindir}/cc.clang 30
%{_sbindir}/alternatives --install %{_bindir}/c++ c++ \
  %{_bindir}/c++.clang 30

%{_sbindir}/alternatives --install %{_bindir}/cc cc \
  %{_bindir}/cc.gcc 60
%{_sbindir}/alternatives --install %{_bindir}/c++ c++ \
  %{_bindir}/c++.gcc 60

%{_sbindir}/alternatives --auto cc
%{_sbindir}/alternatives --auto c++

exit 0
%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove cc %{_bindir}/cc.clang-nogcc
  %{_sbindir}/alternatives --remove cc %{_bindir}/cc.clang-nogcc-with-compiler-rt
  %{_sbindir}/alternatives --remove cc %{_bindir}/cc.clang
  %{_sbindir}/alternatives --remove cc %{_bindir}/cc.gcc
  %{_sbindir}/alternatives --remove c++ %{_bindir}/c++.clang-nogcc
  %{_sbindir}/alternatives --remove c++ %{_bindir}/c++.clang-nogcc-with-compiler-rt
  %{_sbindir}/alternatives --remove c++ %{_bindir}/c++.clang
  %{_sbindir}/alternatives --remove c++ %{_bindir}/c++.gcc
fi
exit 0

%files
%{_bindir}/*
%changelog

