#
# Conditional build:
%bcond_without	tests	# don't perform "make test"
%bcond_with	pthread	# build pthread library (POSIX.1c threading API of GNU Pth)
#
Summary:	The GNU portable threads
Summary(pl):	Przeno¶ne w±tki GNU
Name:		pth
Version:	2.0.2
Release:	1
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/pth/%{name}-%{version}.tar.gz
# Source0-md5:	fc4d81a1dbf3d1af9a099b765f9a1be3
Patch0:		%{name}-am18.patch
URL:		http://www.gnu.org/software/pth/
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution (aka `multithreading') inside event-driven
applications. All threads run in the same address space of the server
application, but each thread has its own individual program-counter,
run-time stack, signal mask and errno variable.

%description -l pl
pth jest bardzo przeno¶n± bibliotek± bazuj±c± na POSIX/ANSI-C dla
platform uniksowych, bazuj±ce na priorytetach dzielenie czasu bez
wyw³aszczenia dla wielu w±tków (czyli wielow±tkowo¶æ) wewn±trz
aplikacji sterowanych zdarzeniami. Wszystkie w±tki dzia³aj± w tej
samej przestrzeni adresowej aplikacji serwera, ale ka¿dy ma swój
w³asny licznik instrukcji, stos, maski sygna³ów i zmienn± errno.

%package devel
Summary:	Header files and development documentation for pth
Summary(pl):	Pliki nag³ówkowe i dokumentacja do pth
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for pth.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do pth.

%package static
Summary:	Static version of the GNU portable threads library
Summary(pl):	Statyczna wersja biblioteki pth
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of the GNU portable threads library.

%description static -l pl
Statyczna wersja biblioteki przeno¶nych w±tków GNU.

%prep
%setup -q
%patch0 -p1

%build
cp -f /usr/share/automake/config.* .

# -fno-strict-aliasing" because mainly pth_mctx.c contains important
# and correct pointer casting constructs which are not acceptable
# in "strict aliasing" for GCC.
export CFLAGS="%{rpmcflags} -fno-strict-aliasing"
%configure \
	%{?with_pthread:--enable-pthread} \
	--enable-optimize

%{__make} pth_p.h
%{__make}
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING contains not only LGPL text
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS README SUPPORT TESTS THANKS USERS
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc HACKING
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_aclocaldir}/pth.m4
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man1/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
