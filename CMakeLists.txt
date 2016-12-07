project(sqlite3)
cmake_minimum_required(VERSION 2.8)
add_library(sqlite3 sqlite3.c)
set_target_properties(sqlite3 PROPERTIES LINKER_LANGUAGE CXX)

