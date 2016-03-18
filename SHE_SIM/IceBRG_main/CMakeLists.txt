# Declare this directory as an Elements module
elements_subdir(IceBRG_main)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
find_package(Boost)
find_package(Eigen3)

# Instruction for creating a C++ library
elements_add_library(IceBRG_main src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen
                     PUBLIC_HEADERS IceBRG_main)
                     