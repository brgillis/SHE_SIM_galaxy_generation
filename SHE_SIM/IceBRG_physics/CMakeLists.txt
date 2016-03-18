# Declare this directory as an Elements module
#   (Replace ExampleModule with the correct name for another module)
elements_subdir(IceBRG_physics)

# Declare Elements module dependencies
#    This module is using of the ElementsKernel module
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
#    The module is using the Boost C++ library
find_package(Boost)
find_package(Eigen)
find_package(IceBRG_main)

# Instruction for creating a C++ library
#    IceBRG is the library name
#    src/lib/*.cpp are the source files
elements_add_library(IceBRG_physics src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen IceBRG_main
                     PUBLIC_HEADERS IceBRG_physics)

# Instruction for Python module installation
elements_install_python_modules()

# Install the configuration files
elements_install_conf_files()

# Instruction for building C++ tests
elements_add_unit_test(IceBRG_physics_test                  
                       tests/src/*_test.cpp
                       LINK_LIBRARIES IceBRG_physics
                       TYPE Boost )