%define build_docs	0

Name:           qbs
Version:        2.4.2
Release:        1
Summary:        Build automation tool
Group:          Development/KDE and Qt
# See LGPL_EXCEPTION.txt
License:        LGPLv2 with exceptions and LGPLv3 with exceptions
URL:            https://wiki.qt.io/qbs
Source0:        https://download.qt.io/official_releases/%{name}/%{version}/%{name}-src-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Help)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Test)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
Obsoletes:  qbs > 4.2.2
Obsoletes:  %{mklibname qbsqtprofilesetup 1} < 1.13.0

%description
Qbs is a tool that helps simplify the build process for developing projects
across multiple platforms. Qbs can be used for any software project, regardless
of programming language, toolkit, or libraries used.

Qbs is an all-in-one tool that generates a build graph from a high-level
project description (like qmake or CMake) and additionally undertakes the task
of executing the commands in the low-level build graph (like make).

%files
%{_bindir}/*
%{_datadir}/qbs/
%{_libdir}/qbs/
%{_libexecdir}/qbs/
#{_mandir}/man1/qbs.1.*

#--------------------------------------------------------------------

%define qbscore_major 2
%define libqbscore %mklibname qbscore %{qbscore_major}

%package -n     %{libqbscore}
Summary:        Qbs Core library
Group:          System/Libraries

%description -n %{libqbscore}
Qbs Core library.

%files -n %{libqbscore}
%{_libdir}/libqbscore.so.%{qbscore_major}{,.*}

#--------------------------------------------------------------------

%define libqbs_d %mklibname %{name} -d

%package -n     %{libqbs_d}
Summary:        Devel files needed to build apps based on %{name}
Group:          Development/KDE and Qt
Requires:       %{libqbscore} = %{EVRD}
Provides:       lib%{name}-devel = %{version}
Provides:       %{name}-devel = %{version}

%description -n %{libqbs_d}
Devel files needed to build apps based on %{name}.

%files -n %{libqbs_d}
%{_includedir}/%{name}/
%{_libdir}/*.so

#------------------------------------------------------------------------------

%if %{build_docs}
%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
License:        GFDL
BuildArch:      noarch
BuildRequires:  qttools5
# This one is required to build QCH-format documentation
# for APIs and tools in this package set
BuildRequires:  qttools5-assistant
Recommends:     qttools5-assistant

%description    doc
HTML documentation for %{name}.

%files doc
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/%{name}.qch
%doc %{_docdir}/%{name}/html/
%endif

#------------------------------------------------------------------------------

%prep
%autosetup -n %{name}-src-%{version} -p1

# We want Qt6, not Qt5
sed -i -e 's, Qt5,,g' CMakeLists.txt

%conf
%cmake \
	-DQT_VERSION_MAJOR=6 \
	-DQBS_LIB_INSTALL_DIR=%{_lib} \
	-DQBS_PLUGINS_INSTALL_BASE=%{_lib} \
	-G Ninja

%build
# LD_LIBRARY_PATH: Because the qbs executable built is itself invoked, and it requires the built qbs libraries
LD_LIBRARY_PATH=$(pwd)/build/%{_lib}:${LD_LIBRARY_PATH} %ninja_build -C build

%install
%ninja_install -C build
