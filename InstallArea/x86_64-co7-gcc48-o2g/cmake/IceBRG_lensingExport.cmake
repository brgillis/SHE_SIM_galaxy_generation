# File automatically generated: DO NOT EDIT.

# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)

add_library(IceBRG_lensing SHARED IMPORTED)
set_target_properties(IceBRG_lensing PROPERTIES
  REQUIRED_INCLUDE_DIRS "ElementsKernel;Boost;Log4CPP;IceBRG_main;Eigen3;IceBRG_physics"
  REQUIRED_LIBRARIES "ElementsKernel;boost_serialization;IceBRG_main;IceBRG_physics;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_SONAME "libIceBRG_lensing.so"
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/libIceBRG_lensing.so"
  )
set(IceBRG_lensing_DEPENDENCIES ElementsKernel;IceBRG_main;IceBRG_physics)
set(IceBRG_lensing_VERSION 1.0)
