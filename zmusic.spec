%define	oname	ZMusic
%define major 	1
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

Name:           zmusic
Version:        1.1.8
Release:        1
Summary:        ZDoom component library for music handling
License:        GPL-3.0-only
Group:          Development/Libraries/C and C++
URL:            https://zdoom.org/

Source:         https://github.com/coelckers/ZMusic/archive/%{version}/%{oname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(libgme)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(zlib)
Suggests:       fluid-soundfont-gm
Suggests:       fluid-soundfont-gs
Suggests:       timidity
Suggests:       timidity-eawpats
# DUMB is modified to read OggVorbis samples
Provides:       bundled(dumb) = 0.9.3

%description
This is the music playback code from gzdoom, which was separated into its own
code repository starting with gzdoom-4.4.0.

%package -n %{libname}
Summary:        ZDoom component library for music handling
Group:          System/Libraries

%description -n %{libname}
This is the music playback code from gzdoom, which was separated into its own
code repository starting with gzdoom-4.4.0.

%package -n %{devname}
Summary:        Headers for the ZMusic library
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{EVRD}

%description -n	%{devname}
This subpackage contains the headers for the zmusic library, which is ZDoom's
music component library.

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
# There is handcrafted assembler, which LTO does not play nice with.
%define _lto_cflags %nil

%ifarch %ix86
# Allow sw to use intrinsics (functions like _mm_set_sd).
# Guarded by cpuid calls by sw.
export CFLAGS="%optflags -msse -msse2"
export CXXFLAGS="%optflags -msse -msse2"
%endif
%cmake -DNO_STRIP=1 \
	-DCMAKE_SHARED_LINKER_FLAGS="" \
	-DCMAKE_EXE_LINKER_FLAGS="" -DCMAKE_MODULE_LINKER_FLAGS="" \
	-DINSTALL_DOCS_PATH="%_defaultdocdir/%name" \
	-DDYN_FLUIDSYNTH=OFF \
	-DDYN_SNDFILE=OFF -DDYN_MPG123=OFF
%make_build

%install
%make_install -C build


%files -n %{libname}
%license licenses/*
%{_libdir}/libzmusic.so.%{major}*
%{_libdir}/libzmusiclite.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libzmusic.so
%{_libdir}/libzmusiclite.so
%{_libdir}/cmake/
