FILE(REMOVE_RECURSE
  "../lib/lib_SHE_SIM.so.dbg"
  "../bin/SHE_SIM_tests.dbg"
  "CMakeFiles/SHE_SIM_tests_dir"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/SHE_SIM_tests_dir.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
