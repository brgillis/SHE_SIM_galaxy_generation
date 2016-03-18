# Declare this directory as an Elements module
elements_subdir(cIceBRGpy)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)

# Declare library dependencies
find_package(IceBRG_main)
find_package(IceBRG_physics)
find_package(IceBRG_lensing)

# Install the configuration files
elements_install_conf_files()
                   