# CMake generated Testfile for 
# Source directory: /home/user/git/she_sim_galaxy_generation/SHE_SIM_galaxy_image_generation
# Build directory: /home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/SHE_SIM_galaxy_image_generation
# 
# This file includes the relevent testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
ADD_TEST(SHE_SIM_galaxy_image_generation.PyTest "/usr/bin/python" "/opt/euclid/Elements/3.10/InstallArea/x86_64-co7-gcc48-o2g/cmake/scripts/env.py" "--xml" "/home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/SheSimBuildEnvironment.xml" "/usr/bin/py.test" "/home/user/git/she_sim_galaxy_generation/SHE_SIM_galaxy_image_generation/tests/python/test_import.py")
SET_TESTS_PROPERTIES(SHE_SIM_galaxy_image_generation.PyTest PROPERTIES  LABELS "SHE_SIM_galaxy_image_generation;Python;UnitTest;PyTest" WORKING_DIRECTORY ".")
