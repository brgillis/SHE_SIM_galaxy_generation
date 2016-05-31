FILE(REMOVE_RECURSE
  "CMakeFiles/rpmbuilddir"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/rpmbuilddir.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
