cmake_minimum_required(VERSION 3.26)

project(HLAndro)

include(FetchContent)

FetchContent_Declare(
  CPM
  GIT_REPOSITORY https://github.com/cpm-cmake/CPM.cmake.git
  GIT_TAG v0.42.0
)

FetchContent_MakeAvailable(CPM)

# set(HL_DIR $ENV{HASHLINK_DIR})
# message(STATUS "Hashlink Dir: ${HL_DIR}")

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/android-bin" CACHE PATH "Default install path" FORCE)
endif()

# main
set(WITH_VM OFF)
set(BUILD_TESTING OFF)

#SDL
CPMAddPackage(
  NAME SDL2
  GITHUB_REPOSITORY libsdl-org/SDL
  GIT_TAG release-2.32.8
)

CPMAddPackage(
  NAME SDL2
  GITHUB_REPOSITORY libsdl-org/SDL
  GIT_TAG release-2.32.8
)

CPMAddPackage(
  NAME PNG
  GITHUB_REPOSITORY pnggroup/libpng
  GIT_TAG v1.6.50
)

# libjpeg-turbo refuses to be used as sub project
# CPMAddPackage(
#   NAME TurboJPEG
#   GITHUB_REPOSITORY libjpeg-turbo/libjpeg-turbo
#   GIT_TAG 3.1.1
# )

# compilcated.. because vorbis expect ogg as a sub directory, fetch content does not do that
# CPMAddPackage(
#   GIT_REPOSITORY https://gitlab.xiph.org/xiph/ogg.git
#   GIT_TAG v1.3.6
# )

# CPMAddPackage(
#   GIT_REPOSITORY https://gitlab.xiph.org/xiph/vorbis.git
#   GIT_TAG v1.3.6
# )

# libraries
# set(WITH_FMT OFF)
# set(WITH_SDL OFF)
# set(WITH_UI OFF)
set(WITH_OPENAL OFF)
set(WITH_SQLITE OFF)
set(WITH_SSL OFF)
set(WITH_UV OFF)
set(WITH_VIDEO OFF)
set(WITH_HEAPS OFF)

add_subdirectory(.. the_hashlink)