# Declare this directory as an Elements module
elements_subdir(SHE_SIM)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)
elements_depends_on_subdirs(IceBRG_main)
elements_depends_on_subdirs(IceBRG_physics)
elements_depends_on_subdirs(IceBRG_lensing)

# Declare library dependencies
find_package(Boost)
find_package(Eigen3)

# Instruction for creating a C++ library
elements_add_library(_SHE_SIM src/lib/*.cpp src/lib/*/*.cpp
                     LINK_LIBRARIES ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing
                     INCLUDE_DIRS ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing SHE_SIM
                     PUBLIC_HEADERS SHE_SIM)

# Instructions for creating a SWIG binding
elements_add_swig_binding(SHE_SIM SHE_SIM/SHE_SIM.i
						  LINK_LIBRARIES ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing _SHE_SIM
						  INCLUDE_DIRS ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing SHE_SIM
						  NO_PUBLIC_HEADERS)

# Instruction for building C++ tests
elements_add_unit_test(SHE_SIM_tests                  
                       tests/src/*_test.cpp
                       LINK_LIBRARIES ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing _SHE_SIM
                       INCLUDE_DIRS ElementsKernel Boost Eigen3 IceBRG_main IceBRG_physics IceBRG_lensing SHE_SIM
                       TYPE Boost )