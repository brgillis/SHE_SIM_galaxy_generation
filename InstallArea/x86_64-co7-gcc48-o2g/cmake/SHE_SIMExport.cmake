# File automatically generated: DO NOT EDIT.

# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)

add_library(_SHE_SIM SHARED IMPORTED)
set_target_properties(_SHE_SIM PROPERTIES
  REQUIRED_INCLUDE_DIRS "ElementsKernel;Boost;Log4CPP;IceBRG_main;Eigen3;IceBRG_physics;IceBRG_lensing;SHE_SIM"
  REQUIRED_LIBRARIES "ElementsKernel;IceBRG_main;IceBRG_physics;IceBRG_lensing;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so;boost_serialization"
  IMPORTED_SONAME "lib_SHE_SIM.so"
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/lib_SHE_SIM.so"
  )
add_executable(SHE_SIM_tests IMPORTED)
set_target_properties(SHE_SIM_tests PROPERTIES
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/bin/SHE_SIM_tests"
  )
set(SHE_SIM_DEPENDENCIES ElementsKernel;IceBRG_main;IceBRG_physics;IceBRG_lensing)
set(SHE_SIM_VERSION 1.0)
