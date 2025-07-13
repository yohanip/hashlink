cmake_minimum_required(VERSION 3.26)

project(HLAndro)

# set(HL_DIR $ENV{HASHLINK_DIR})
# message(STATUS "Hashlink Dir: ${HL_DIR}")

# main
set(WITH_VM OFF)
set(BUILD_TESTING OFF)

find_package(Threads REQUIRED)

# libraries
set(WITH_FMT OFF)
set(WITH_OPENAL OFF)
set(WITH_SDL OFF)
set(WITH_SQLITE OFF)
set(WITH_SSL OFF)
set(WITH_UI OFF)
set(WITH_UV OFF)
set(WITH_VIDEO OFF)
set(WITH_HEAPS OFF)

add_subdirectory(.. the_hashlink)