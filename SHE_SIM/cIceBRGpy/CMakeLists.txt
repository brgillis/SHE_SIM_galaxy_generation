# Declare this directory as an Elements module
elements_subdir(cIceBRGpy)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)
elements_depends_on_subdirs(IceBRG_main)
elements_depends_on_subdirs(IceBRG_physics)
elements_depends_on_subdirs(IceBRG_lensing)

# Declare library dependencies

# Instruction for creating a C++ library

# Instructions for creating a SWIG binding
elements_add_swig_binding(cIceBRGpy cIceBRGpy/cIceBRGpy.i
                          LINK_LIBRARIES IceBRG_main IceBRG_physics IceBRG_lensing
                          INCLUDE_DIRS IceBRG_main IceBRG_physics IceBRG_lensing
						  NO_PUBLIC_HEADERS)

