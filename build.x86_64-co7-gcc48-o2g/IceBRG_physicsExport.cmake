# File automatically generated: DO NOT EDIT.

# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)

add_library(IceBRG_physics SHARED IMPORTED)
set_target_properties(IceBRG_physics PROPERTIES
  REQUIRED_INCLUDE_DIRS "ElementsKernel;Boost;Log4CPP;IceBRG_main;Eigen3"
  REQUIRED_LIBRARIES "ElementsKernel;IceBRG_main;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_SONAME "libIceBRG_physics.so"
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/libIceBRG_physics.so"
  )
add_executable(IceBRG_physics_test IMPORTED)
set_target_properties(IceBRG_physics_test PROPERTIES
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/bin/IceBRG_physics_test"
  )
set(IceBRG_physics_DEPENDENCIES ElementsKernel;IceBRG_main)
set(IceBRG_physics_VERSION 1.0)
