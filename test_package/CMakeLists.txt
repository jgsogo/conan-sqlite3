project(sqlite3_test)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

message("libs: ${CONAN_LIBS}")

add_executable(test test.cpp)
set_target_properties(test PROPERTIES LINKER_LANGUAGE CXX)
include_directories(${CONAN_INCLUDE_DIRS})
target_link_libraries(test ${CONAN_LIBS})
