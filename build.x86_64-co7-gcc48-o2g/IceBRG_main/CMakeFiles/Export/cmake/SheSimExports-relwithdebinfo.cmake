#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "IceBRG_main" for configuration "RelWithDebInfo"
set_property(TARGET IceBRG_main APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(IceBRG_main PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "ElementsKernel;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libIceBRG_main.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libIceBRG_main.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS IceBRG_main )
list(APPEND _IMPORT_CHECK_FILES_FOR_IceBRG_main "${_IMPORT_PREFIX}/lib/libIceBRG_main.so" )

# Import target "IceBRG_physics" for configuration "RelWithDebInfo"
set_property(TARGET IceBRG_physics APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(IceBRG_physics PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "ElementsKernel;IceBRG_main;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libIceBRG_physics.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libIceBRG_physics.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS IceBRG_physics )
list(APPEND _IMPORT_CHECK_FILES_FOR_IceBRG_physics "${_IMPORT_PREFIX}/lib/libIceBRG_physics.so" )

# Import target "IceBRG_physics_test" for configuration "RelWithDebInfo"
set_property(TARGET IceBRG_physics_test APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(IceBRG_physics_test PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/IceBRG_physics_test"
  )

list(APPEND _IMPORT_CHECK_TARGETS IceBRG_physics_test )
list(APPEND _IMPORT_CHECK_FILES_FOR_IceBRG_physics_test "${_IMPORT_PREFIX}/bin/IceBRG_physics_test" )

# Import target "IceBRG_lensing" for configuration "RelWithDebInfo"
set_property(TARGET IceBRG_lensing APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(IceBRG_lensing PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "ElementsKernel;boost_serialization;IceBRG_main;IceBRG_physics;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libIceBRG_lensing.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libIceBRG_lensing.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS IceBRG_lensing )
list(APPEND _IMPORT_CHECK_FILES_FOR_IceBRG_lensing "${_IMPORT_PREFIX}/lib/libIceBRG_lensing.so" )

# Import target "_SHE_SIM" for configuration "RelWithDebInfo"
set_property(TARGET _SHE_SIM APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(_SHE_SIM PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "ElementsKernel;IceBRG_main;IceBRG_physics;IceBRG_lensing;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so;boost_serialization"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/lib_SHE_SIM.so"
  IMPORTED_SONAME_RELWITHDEBINFO "lib_SHE_SIM.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS _SHE_SIM )
list(APPEND _IMPORT_CHECK_FILES_FOR__SHE_SIM "${_IMPORT_PREFIX}/lib/lib_SHE_SIM.so" )

# Import target "SHE_SIM_tests" for configuration "RelWithDebInfo"
set_property(TARGET SHE_SIM_tests APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(SHE_SIM_tests PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/SHE_SIM_tests"
  )

list(APPEND _IMPORT_CHECK_TARGETS SHE_SIM_tests )
list(APPEND _IMPORT_CHECK_FILES_FOR_SHE_SIM_tests "${_IMPORT_PREFIX}/bin/SHE_SIM_tests" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
