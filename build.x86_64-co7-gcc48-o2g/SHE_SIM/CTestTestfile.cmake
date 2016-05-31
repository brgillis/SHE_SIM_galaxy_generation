# CMake generated Testfile for 
# Source directory: /home/user/git/she_sim_galaxy_generation/SHE_SIM
# Build directory: /home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/SHE_SIM
# 
# This file includes the relevent testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
ADD_TEST(SHE_SIM.SHE_SIM_tests "/usr/bin/python" "/opt/euclid/Elements/3.10/InstallArea/x86_64-co7-gcc48-o2g/cmake/scripts/env.py" "--xml" "/home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/SheSimBuildEnvironment.xml" "SHE_SIM_tests")
SET_TESTS_PROPERTIES(SHE_SIM.SHE_SIM_tests PROPERTIES  LABELS "UnitTest;SHE_SIM;Binary;Boost" WORKING_DIRECTORY ".")
