# Declare this directory as an Elements module
elements_subdir(SHE_SIM_galaxy_image_generation)

# Declare Elements module dependencies
elements_depends_on_subdirs(ElementsKernel)
elements_depends_on_subdirs(cIceBRGpy)
elements_depends_on_subdirs(IceBRGpy)
elements_depends_on_subdirs(SHE_SIM)

# Declare library dependencies

# Instruction for Python module installation
elements_install_python_modules()

# Install the configuration files
elements_install_conf_files()

# Instruction for creating a Python executable
elements_add_python_program(generate_galaxy_images SHE_SIM_galaxy_image_generation.gen_galsim_images)
                