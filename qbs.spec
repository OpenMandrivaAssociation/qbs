%define debug_package %{nil}

Name: qbs
Version: 1.12.0
Release: 1
Source0: https://download.qt.io/official_releases/qbs/%{version}/qbs-src-%{version}.tar.gz
Source10: %{name}.rpmlintrc
Summary: The QBS Build System
URL: http://wiki.qt.io/Qbs
License: GPL
Group: Development/Tools
BuildRequires: qmake5
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Script)
BuildRequires: cmake(Qt5Xml)
BuildRequires: cmake(Qt5Test)

%define devname %mklibname %{name} -d

%libpackage qbscore 1
%libpackage qbsqtprofilesetup 1

%description
The QBS Build System.

%package -n %{devname}
Summary: Development files for the QBS Build System
Group: Development/Tools
Requires: %{name} = %{EVRD}

%description -n %{devname}
Development files for the QBS Build System.

%prep
%setup -qn %{name}-src-%{version}
%{_libdir}/qt5/bin/qmake -r qbs.pro QBS_INSTALL_PREFIX=%{_prefix} QBS_LIBRARY_DIRNAME=%{_lib}

%build
%make

%install
%makeinstall INSTALL_ROOT=%{buildroot}

%files
%{_bindir}/*
%{_libexecdir}/qbs
%{_libdir}/qbs
%dir %{_datadir}/qbs
%{_datadir}/qbs/imports
%{_datadir}/qbs/modules
%{_datadir}/qbs/python
%{_mandir}/man1/qbs.1*

%files -n %{devname}
%{_includedir}/qbs
%{_datadir}/qbs/examples
%{_libdir}/*.so
%{_libdir}/*.prl
