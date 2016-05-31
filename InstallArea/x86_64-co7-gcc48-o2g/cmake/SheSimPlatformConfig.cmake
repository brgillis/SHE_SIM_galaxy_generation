# File automatically generated: DO NOT EDIT.

# Get the exported informations about the targets
get_filename_component(_dir ${CMAKE_CURRENT_LIST_FILE} PATH)
#include(${_dir}/SheSimExports.cmake)

# Set useful properties
get_filename_component(_dir ${_dir} PATH)
set(SheSim_INCLUDE_DIRS ${_dir}/include)
set(SheSim_LIBRARY_DIRS ${_dir}/lib)

set(SheSim_BINARY_PATH ${_dir}/bin ${_dir}/scripts)
set(SheSim_PYTHON_PATH ${_dir}/python)
set(SheSim_CONF_PATH ${_dir}/conf)
set(SheSim_AUX_PATH ${_dir}/auxdir)

set(SheSim_COMPONENT_LIBRARIES )
set(SheSim_LINKER_LIBRARIES IceBRG_main;IceBRG_physics;IceBRG_lensing;_SHE_SIM)

set(SheSim_ENVIRONMENT PREPEND;PATH;/usr/lib64/ccache;PREPEND;PATH;\${.}/scripts;PREPEND;PATH;\${.}/bin;PREPEND;LD_LIBRARY_PATH;\${.}/lib;PREPEND;PYTHONPATH;\${.}/python;PREPEND;PYTHONPATH;\${.}/python/lib-dynload;PREPEND;ELEMENTS_CONF_PATH;\${.}/conf;PREPEND;ELEMENTS_AUX_PATH;\${.}/auxdir;SET;SHESIM_PROJECT_ROOT;\${.}/../..;SET;ICEBRG_MAINROOT;\${SHESIM_PROJECT_ROOT}/IceBRG_main;SET;ICEBRG_PHYSICSROOT;\${SHESIM_PROJECT_ROOT}/IceBRG_physics;SET;ICEBRG_LENSINGROOT;\${SHESIM_PROJECT_ROOT}/IceBRG_lensing;SET;SHE_SIMROOT;\${SHESIM_PROJECT_ROOT}/SHE_SIM;SET;CICEBRGPYROOT;\${SHESIM_PROJECT_ROOT}/cIceBRGpy;SET;ICEBRGPYROOT;\${SHESIM_PROJECT_ROOT}/icebrgpy;SET;SHE_SIM_GALAXY_IMAGE_GENERATIONROOT;\${SHESIM_PROJECT_ROOT}/SHE_SIM_galaxy_image_generation)

set(SheSim_EXPORTED_SUBDIRS)
foreach(p IceBRG_main;IceBRG_physics;IceBRG_lensing;SHE_SIM;cIceBRGpy;icebrgpy;SHE_SIM_galaxy_image_generation)
  get_filename_component(pn ${p} NAME)
  if(EXISTS ${_dir}/cmake/${pn}Export.cmake)
    set(SheSim_EXPORTED_SUBDIRS ${SheSim_EXPORTED_SUBDIRS} ${p})
  endif()
endforeach()

set(SheSim_OVERRIDDEN_SUBDIRS )
