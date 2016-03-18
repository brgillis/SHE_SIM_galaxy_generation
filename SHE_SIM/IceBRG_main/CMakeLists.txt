# Declare this directory as an Elements module
#   (Replace ExampleModule with the correct name for another module)
elements_subdir(IceBRG_main)

# Declare Elements module dependencies
#    This module is using of the ElementsKernel module
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
#    The module is using the Boost C++ library
find_package(Boost)
find_package(Eigen3)

# Instruction for creating a C++ library
#    IceBRG is the library name
#    src/lib/*.cpp are the source files
elements_add_library(IceBRG_main src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen
                     PUBLIC_HEADERS IceBRG_main)
                     