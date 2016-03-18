# Declare this directory as an Elements module
elements_subdir(cIceBRGpy)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
find_package(IceBRG_main)
find_package(IceBRG_physics)
find_package(IceBRG_lensing)

# Instruction for creating a C++ library
elements_add_library(cIceBRGpy src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen IceBRG_main IceBRG_physics IceBRG_lensing
                     PUBLIC_HEADERS cIceBRGpy)

# Instructions for creating a SWIG binding
elements_add_swig_binding(cIceBRGpy cIceBRGpy/cIceBRGpy.i
						  LINK_LIBRARIES cIceBRGpy
						  INCLUDE_DIRS cIceBRGpy
						  NO_PUBLIC_HEADERS)

# Install the configuration files
elements_install_conf_files()
