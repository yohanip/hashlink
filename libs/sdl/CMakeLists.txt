if(WIN32)
    set(SDL2_PATH ${INCLUDES_BASE_DIR}/sdl)
endif()

# find_package(SDL2 REQUIRED)

if(ANDROID)
    list(APPEND srcs sdl.c)
else()
    list(APPEND srcs sdl.c gl.c)
endif(ANDROID)

# make sure SDL are at release-2.32.8
add_subdirectory($ENV{CXX_WELLKNOWN_ROOT}/SDL mysdl)

add_library(sdl.hdll SHARED
    ${srcs}
)
set_as_hdll(sdl)
target_include_directories(sdl.hdll
    PRIVATE
    SDL2::SDL2-static
    ${INCLUDES_BASE_DIR}/gl
)
target_link_libraries(sdl.hdll
    PRIVATE libhl
    PRIVATE SDL2::SDL2-static
)

if(WIN32)
    target_link_libraries(sdl.hdll
        winmm
        opengl32
    )
endif()

if(APPLE OR LINUX)
    find_package(OpenGL REQUIRED)
    if(TARGET OpenGL::GL)
        target_link_libraries(sdl.hdll PRIVATE OpenGL::GL)
    else()
        if(EMSCRIPTEN AND OPENGL_gl_LIBRARY STREQUAL "nul")
            set(OPENGL_gl_LIBRARY GL)
        endif()
        # emscripten's FindOpenGL.cmake does not create OpenGL::GL
        target_link_libraries(sdl.hdll PRIVATE ${OPENGL_gl_LIBRARY})
    endif()
endif()

# get_target_property(_libs sdl.hdll LINK_LIBRARIES)
# message(FATAL_ERROR "sdl.hdll libraries:${_libs}")

install(
    TARGETS sdl.hdll
    DESTINATION ${HDLL_DESTINATION}
)
