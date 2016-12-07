project(sqlite3_test)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

add_executable(test test.c)
include_directories(${CONAN_INCLUDE_DIRS})
target_link_libraries(test ${CONAN_LIBS})
