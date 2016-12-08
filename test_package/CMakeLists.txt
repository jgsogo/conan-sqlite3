project(sqlite3_test)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package("SQLite3")

if(SQLITE3_FOUND)
    add_executable(test test.cpp)
    include_directories(${SQLITE3_INCLUDE_DIRS})
    target_link_libraries(test PUBLIC ${SQLITE3_LIBRARIES})
else()
    message(FATAL_ERROR "SQLite3 not found")
endif()

