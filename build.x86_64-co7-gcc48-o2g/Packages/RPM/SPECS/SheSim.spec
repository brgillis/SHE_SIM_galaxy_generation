# -*- rpm-spec -*-
Summary:        Euclid SheSim Project
Name:           SheSim
Version:        1.0
Release:        1%{?dist}
License:        Public Domain
Group:          Development/Tools
Source:         SheSim-1.0.tar.gz
Vendor:         The Euclid Consortium


BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: gcc > 4.7, cmake >= 2.6, Elements-devel = 3.10

Requires: python, Elements = 3.10
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define bin_tag x86_64-co7-gcc48-o2g
%define _proj_base_dir /opt/euclid
%define _proj_name_dir %{_proj_base_dir}/%{name}
%define _proj_vers_dir %{_proj_name_dir}/%{version}
%define _proj_ia_dir %{_proj_vers_dir}/InstallArea
%define _prefix %{_proj_ia_dir}/%{bin_tag}
%define build_dir_name build.x86_64-co7-gcc48-o2g
%define libdir %{_prefix}/lib
%define pydir %{_prefix}/python
%define scriptsdir %{_prefix}/scripts
%define cmakedir %{_prefix}/cmake
%define confdir %{_prefix}/conf
%define auxdir %{_prefix}/auxdir

%define debug_package %{nil}

%description
Please provide a description of the project.

%package devel
Group:  Development/Libraries
Summary: The development part of the %{name} package
Requires: cmake >= 2.6, %{name} = %{version}-%{release}, Elements-devel = 3.10

%description devel
The development part of the %{name} package.

%package debuginfo
Summary: Debug information for package %{name}
Requires: %{name} = %{version}-%{release}, Elements-debuginfo = 3.10

%description debuginfo
Debug information for package %{name}

%prep
%setup -q

%build
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
if [[ -z "$EUCLID_BASE" ]]; then
  export CMAKE_PROJECT_PATH=/opt/euclid
else
  export CMAKE_PROJECT_PATH=$EUCLID_BASE
fi
export CMAKE_PREFIX_PATH=$PWD/cmake:/usr/share/EuclidEnv/cmake
toolchain_name=ElementsToolChain.cmake
if [[ -f "${PWD}/cmake/${toolchain_name}" ]]; then
  toolchain_file=${PWD}/cmake/${toolchain_name}
else
  if [[ -f "/usr/share/EuclidEnv/cmake/${toolchain_name}" ]]; then
    toolchain_file=/usr/share/EuclidEnv/cmake/${toolchain_name}
  fi
fi
%__mkdir -p %{build_dir_name}
cd %{build_dir_name}
if [[ -z "${toolchain_file}" ]]; then
  %cmake  ../
else
  %cmake  -DCMAKE_TOOLCHAIN_FILE=${toolchain_file} ../
fi
%__make VERBOSE=1 %{?_smp_mflags} all

%install
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
if [[ -z "$EUCLID_BASE" ]]; then
  export CMAKE_PROJECT_PATH=/opt/euclid
else
  export CMAKE_PROJECT_PATH=$EUCLID_BASE
fi
export CMAKE_PREFIX_PATH=$PWD/cmake:/usr/share/EuclidEnv/cmake
cd %{build_dir_name}
%__make install VERBOSE=1 DESTDIR=$RPM_BUILD_ROOT

%clean
%__rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
for d in  %{_proj_ia_dir}  %{_proj_vers_dir} %{_proj_name_dir}; do
  if [[ -d "${d}" ]]; then
    if [[ ! "$(ls -A ${d})" ]]; then
      echo "Removing the ${d} empty directory ..."
      rmdir ${d}
    fi
  fi
done

%files
%defattr(-,root,root,-)
%dir %{_prefix}
%{_prefix}/SheSimEnvironment.xml
%{_prefix}/manifest.xml
%dir %{_bindir}
%{_bindir}/IceBRG_physics_test
%{_bindir}/SHE_SIM_tests
%dir %{libdir}
%{libdir}/libIceBRG_lensing.so
%{libdir}/libIceBRG_main.so
%{libdir}/libIceBRG_physics.so
%{libdir}/lib_SHE_SIM.so
%{scriptsdir}
%{auxdir}
%{confdir}
%{pydir}

%files devel
%defattr(-,root,root,-)
%{_prefix}/SheSimBuildEnvironment.xml
%{_prefix}/SheSimConfig.cmake
%{_prefix}/SheSimConfigVersion.cmake
%{_includedir}
%{cmakedir}

%files debuginfo
%defattr(-,root,root,-)
%{_bindir}/IceBRG_physics_test.dbg
%{_bindir}/SHE_SIM_tests.dbg
%{libdir}/libIceBRG_lensing.so.dbg
%{libdir}/libIceBRG_main.so.dbg
%{libdir}/libIceBRG_physics.so.dbg
%{libdir}/lib_SHE_SIM.so.dbg
