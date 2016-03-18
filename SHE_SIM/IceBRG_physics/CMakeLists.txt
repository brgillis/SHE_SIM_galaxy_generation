# Declare this directory as an Elements module
elements_subdir(IceBRG_physics)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)
elements_depends_on_subdirs(IceBRG_main)

# Declare library dependencies
find_package(Boost)
find_package(Eigen3)

# Instruction for creating a C++ library
elements_add_library(IceBRG_physics src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen IceBRG_main
                     PUBLIC_HEADERS IceBRG_physics)

# Instruction for building C++ tests
elements_add_unit_test(IceBRG_physics_test                  
                       tests/src/*_test.cpp
                       LINK_LIBRARIES IceBRG_physics
                       TYPE Boost )