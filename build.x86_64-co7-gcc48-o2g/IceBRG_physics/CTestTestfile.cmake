# CMake generated Testfile for 
# Source directory: /home/user/git/she_sim_galaxy_generation/IceBRG_physics
# Build directory: /home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/IceBRG_physics
# 
# This file includes the relevent testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
ADD_TEST(IceBRG_physics.IceBRG_physics_test "/usr/bin/python" "/opt/euclid/Elements/3.10/InstallArea/x86_64-co7-gcc48-o2g/cmake/scripts/env.py" "--xml" "/home/user/git/she_sim_galaxy_generation/build.x86_64-co7-gcc48-o2g/SheSimBuildEnvironment.xml" "IceBRG_physics_test")
SET_TESTS_PROPERTIES(IceBRG_physics.IceBRG_physics_test PROPERTIES  LABELS "UnitTest;IceBRG_physics;Binary;Boost" WORKING_DIRECTORY ".")
