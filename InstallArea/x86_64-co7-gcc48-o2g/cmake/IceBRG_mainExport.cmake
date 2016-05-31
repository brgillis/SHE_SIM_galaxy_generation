# File automatically generated: DO NOT EDIT.

# Compute the installation prefix relative to this file.
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)

add_library(IceBRG_main SHARED IMPORTED)
set_target_properties(IceBRG_main PROPERTIES
  REQUIRED_INCLUDE_DIRS "ElementsKernel;Boost;Log4CPP;Eigen3"
  REQUIRED_LIBRARIES "ElementsKernel;dl;/usr/lib64/libboost_filesystem-mt.so;/usr/lib64/libboost_thread-mt.so;/usr/lib64/libboost_program_options-mt.so;/usr/lib64/libboost_system-mt.so;/usr/lib64/libboost_regex-mt.so;/usr/lib64/liblog4cpp.so"
  IMPORTED_SONAME "libIceBRG_main.so"
  IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/libIceBRG_main.so"
  )
set(IceBRG_main_DEPENDENCIES ElementsKernel)
set(IceBRG_main_VERSION 1.0)
