# Declare this directory as an Elements module
elements_subdir(IceBRG_lensing)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)
elements_depends_on_subdirs(IceBRG_main)
elements_depends_on_subdirs(IceBRG_physics)

# Declare library dependencies
find_package(Boost)
find_package(Eigen3)

# Instruction for creating a C++ library
elements_add_library(IceBRG_lensing src/lib/*.cpp src/lib/*/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost boost_serialization Eigen3 IceBRG_main IceBRG_physics
                     INCLUDE_DIRS ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics
                     PUBLIC_HEADERS IceBRG_lensing)
