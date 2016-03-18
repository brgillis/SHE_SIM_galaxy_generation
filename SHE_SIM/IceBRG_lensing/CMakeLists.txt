# Declare this directory as an Elements module
#   (Replace ExampleModule with the correct name for another module)
elements_subdir(IceBRG_lensing)

# Declare Elements module dependencies
#    This module is using of the ElementsKernel module
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
find_package(Boost)
find_package(Eigen)
find_package(IceBRG_main)
find_package(IceBRG_physics)

# Instruction for creating a C++ library
elements_add_library(IceBRG_lensing src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen IceBRG_main IceBRG_physics
                     PUBLIC_HEADERS IceBRG_lensing)

# Instruction for Python module installation
elements_install_python_modules()

# Install the configuration files
elements_install_conf_files()
                 