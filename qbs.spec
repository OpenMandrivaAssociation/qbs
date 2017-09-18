%define debug_package %{nil}

Name: qbs
Version: 1.9.0
Release: 1
Source0: https://download.qt.io/official_releases/qbs/%{version}/qbs-src-%{version}.tar.gz
Source10: %{name}.rpmlintrc
Summary: The QBS Build System
URL: http://wiki.qt.io/Qbs
License: GPL
Group: Development/Tools
BuildRequires: qmake5

%define devname %mklibname %{name} -d

%libpackage qbscore 1
%libpackage qbsqtprofilesetup 1

%description
The QBS Build System

%package -n %{devname}
Summary: Development files for the QBS Build System
Group: Development/Tools
Requires: %{name} = %{EVRD}

%description -n %{devname}
Development files for the QBS Build System

%prep
%setup -qn dist/%{name}-src-%{version}
qmake -r qbs.pro QBS_INSTALL_PREFIX=%{_prefix} QBS_LIBRARY_DIRNAME=%{_lib}

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

%files -n %{devname}
%{_includedir}/qbs
%{_datadir}/qbs/examples
%{_libdir}/*.so
%{_libdir}/*.prl
