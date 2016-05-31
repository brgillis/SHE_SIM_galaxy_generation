# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. The list of available CPACK_xxx variables and their associated
# documentation may be obtained using
#  cpack --help-variable-list
#
# Some variables are common to all generators (e.g. CPACK_PACKAGE_NAME)
# and some are specific to a generator
# (e.g. CPACK_NSIS_EXTRA_INSTALL_COMMANDS). The generator specific variables
# usually begin with CPACK_<GENNAME>_xxxx.


SET(CPACK_BINARY_BUNDLE "")
SET(CPACK_BINARY_CYGWIN "")
SET(CPACK_BINARY_DEB "")
SET(CPACK_BINARY_DRAGNDROP "")
SET(CPACK_BINARY_NSIS "")
SET(CPACK_BINARY_OSXX11 "")
SET(CPACK_BINARY_PACKAGEMAKER "")
SET(CPACK_BINARY_RPM "")
SET(CPACK_BINARY_STGZ "")
SET(CPACK_BINARY_TBZ2 "")
SET(CPACK_BINARY_TGZ "")
SET(CPACK_BINARY_TZ "")
SET(CPACK_BINARY_WIX "")
SET(CPACK_BINARY_ZIP "")
SET(CPACK_CMAKE_GENERATOR "Unix Makefiles")
SET(CPACK_COMPONENT_UNSPECIFIED_HIDDEN "TRUE")
SET(CPACK_COMPONENT_UNSPECIFIED_REQUIRED "TRUE")
SET(CPACK_GENERATOR "TGZ;TBZ2;TZ")
SET(CPACK_IGNORE_FILES "/InstallArea/;/build\\..*/;/build.x86_64-co7-gcc48-o2g/;/\\.svn/;/\\.settings/;\\..*project;\\.gitignore")
SET(CPACK_INSTALLED_DIRECTORIES "/home/user/git/she_sim_galaxy_generation;/")
SET(CPACK_INSTALL_CMAKE_PROJECTS "")
SET(CPACK_INSTALL_PREFIX "/home/user/git/she_sim_galaxy_generation/InstallArea/x86_64-co7-gcc48-o2g")
SET(CPACK_MODULE_PATH "/opt/euclid/Elements/3.10/InstallArea/x86_64-co7-gcc48-o2g/cmake;/opt/euclid/Elements/3.10/InstallArea/x86_64-co7-gcc48-o2g/cmake/modules;/usr/share/EuclidEnv/cmake;/usr/share/EuclidEnv/cmake/modules")
SET(CPACK_NSIS_DISPLAY_NAME "SheSim 1.0")
SET(CPACK_NSIS_INSTALLER_ICON_CODE "")
SET(CPACK_NSIS_INSTALLER_MUI_ICON_CODE "")
SET(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
SET(CPACK_NSIS_PACKAGE_NAME "SheSim 1.0")
SET(CPACK_OUTPUT_CONFIG_FILE "/home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/CPackConfig.cmake")
SET(CPACK_PACKAGE_DEFAULT_LOCATION "/")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "/usr/share/cmake/Templates/CPack.GenericDescription.txt")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "SheSim built using CMake")
SET(CPACK_PACKAGE_FILE_NAME "SheSim-1.0-Source")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "SheSim 1.0")
SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "SheSim 1.0")
SET(CPACK_PACKAGE_NAME "SheSim")
SET(CPACK_PACKAGE_RELEASE "1")
SET(CPACK_PACKAGE_RELOCATABLE "true")
SET(CPACK_PACKAGE_VENDOR "The Euclid Consortium")
SET(CPACK_PACKAGE_VERSION "1.0")
SET(CPACK_PACKAGE_VERSION_MAJOR "1")
SET(CPACK_PACKAGE_VERSION_MINOR "0")
SET(CPACK_PACKAGE_VERSION_PATCH "1")
SET(CPACK_PACKAGING_INSTALL_PREFIX "/opt/euclid/SheSim/1.0/InstallArea/x86_64-co7-gcc48-o2g")
SET(CPACK_RESOURCE_FILE_LICENSE "/usr/share/cmake/Templates/CPack.GenericLicense.txt")
SET(CPACK_RESOURCE_FILE_README "/usr/share/cmake/Templates/CPack.GenericDescription.txt")
SET(CPACK_RESOURCE_FILE_WELCOME "/usr/share/cmake/Templates/CPack.GenericWelcome.txt")
SET(CPACK_RPM_DEBINFO_FILES "%files debuginfo
%defattr(-,root,root,-)
%{_bindir}/IceBRG_physics_test.dbg
%{_bindir}/SHE_SIM_tests.dbg
%{libdir}/libIceBRG_lensing.so.dbg
%{libdir}/libIceBRG_main.so.dbg
%{libdir}/libIceBRG_physics.so.dbg
%{libdir}/lib_SHE_SIM.so.dbg")
SET(CPACK_RPM_DEVEL_FILES "%files devel
%defattr(-,root,root,-)
%{_prefix}/SheSimBuildEnvironment.xml
%{_prefix}/SheSimConfig.cmake
%{_prefix}/SheSimConfigVersion.cmake
%{_includedir}
%{cmakedir}")
SET(CPACK_RPM_FILE_NAME "SheSim-1.0-1.x86_64")
SET(CPACK_RPM_PACKAGE_ARCHITECTURE "x86_64")
SET(CPACK_RPM_PACKAGE_DESCRIPTION "Please provide a description of the project.")
SET(CPACK_RPM_PACKAGE_NAME "SheSim")
SET(CPACK_RPM_PACKAGE_RELOCATABLE "TRUE")
SET(CPACK_RPM_REGULAR_FILES "%files
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
%{pydir}")
SET(CPACK_SET_DESTDIR "OFF")
SET(CPACK_SOURCE_CYGWIN "")
SET(CPACK_SOURCE_GENERATOR "TGZ;TBZ2;TZ")
SET(CPACK_SOURCE_IGNORE_FILES "/InstallArea/;/build\\..*/;/build.x86_64-co7-gcc48-o2g/;/\\.svn/;/\\.settings/;\\..*project;\\.gitignore")
SET(CPACK_SOURCE_INSTALLED_DIRECTORIES "/home/user/git/she_sim_galaxy_generation;/")
SET(CPACK_SOURCE_OUTPUT_CONFIG_FILE "/home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/CPackSourceConfig.cmake")
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "SheSim-1.0-Source")
SET(CPACK_SOURCE_TBZ2 "ON")
SET(CPACK_SOURCE_TGZ "ON")
SET(CPACK_SOURCE_TOPLEVEL_TAG "x86_64-co7-gcc48-o2g-Source")
SET(CPACK_SOURCE_TZ "ON")
SET(CPACK_SOURCE_ZIP "OFF")
SET(CPACK_STRIP_FILES "")
SET(CPACK_SYSTEM_NAME "x86_64-co7-gcc48-o2g")
SET(CPACK_TOPLEVEL_TAG "x86_64-co7-gcc48-o2g-Source")
SET(CPACK_WIX_SIZEOF_VOID_P "8")
