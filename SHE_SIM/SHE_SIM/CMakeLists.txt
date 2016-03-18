# Declare this directory as an Elements module
elements_subdir(SHE_SIM)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
find_package(Boost)
find_package(Eigen)
find_package(IceBRG_main)
find_package(IceBRG_physics)
find_package(IceBRG_lensing)

# Instruction for creating a C++ library
elements_add_library(SHE_SIM src/lib/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen IceBRG_main IceBRG_physics IceBRG_lensing
                     PUBLIC_HEADERS SHE_SIM)

# Install the configuration files
elements_install_conf_files()

# Instruction for building C++ tests
elements_add_unit_test(SHE_SIM_tests                  
                       tests/src/*_test.cpp
                       LINK_LIBRARIES Boost Eigen IceBRG_main IceBRG_physics IceBRG_lensing
                       TYPE Boost )