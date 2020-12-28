%define build_docs	0

Name:           qbs
Version:        1.18.0
Release:        1
Summary:        Qt5 Build System
Group:          Development/KDE and Qt
# See LGPL_EXCEPTION.txt
License:        LGPLv2 with exceptions and LGPLv3 with exceptions
URL:            https://wiki.qt.io/qbs
Source0:        https://download.qt.io/official_releases/%{name}/%{version}/%{name}-src-%{version}.tar.gz
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
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
%{_mandir}/man1/qbs.1.*

#--------------------------------------------------------------------

%define qbscore_major 1
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
%{_libdir}/*.prl

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

%build
%qmake_qt5 \
  QBS_INSTALL_PREFIX=%{_prefix} \
  QBS_LIBRARY_DIRNAME=%{_lib} \
  QBS_LIBEXEC_INSTALL_DIR=%{_libexecdir}/%{name} \
  QBS_RELATIVE_LIBEXEC_PATH=../libexec/%{name} \
  CONFIG+=qbs_enable_project_file_updates \
  CONFIG+=qbs_disable_rpath \
  CONFIG+=qbs_enable_unit_tests \
  CONFIG+=nostrip \
  QMAKE_LFLAGS="-Wl,--as-needed" \
  qbs.pro
# LD_LIBRARY_PATH: Because the qbs executable built is itself invoked, and it requires the built qbs libraries
LD_LIBRARY_PATH=%{_lib} %make_build

%if %{build_docs}
%make_build docs
%make_build html_docs
%endif

%install
%make_install INSTALL_ROOT=%{buildroot}

%if %{build_docs}
%make_install install_docs INSTALL_ROOT=%{buildroot}
%endif
