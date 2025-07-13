if(WIN32)
    set(SDL2_PATH ${INCLUDES_BASE_DIR}/sdl)
endif()
find_package(SDL2 REQUIRED)

list(APPEND srcs sdl.c)

if(!ANDROID)
    list(APPEND srcs gl.c)
endif(!ANDROID)


add_library(sdl.hdll SHARED
    ${srcs}
)
set_as_hdll(sdl)
target_include_directories(sdl.hdll
    PRIVATE
    SDL2::SDL2
    ${INCLUDES_BASE_DIR}/gl
)
target_link_libraries(sdl.hdll
    libhl
    SDL2::SDL2
)

if(WIN32)
    target_link_libraries(sdl.hdll
        winmm
        opengl32
    )
endif()

if(APPLE OR LINUX)
    find_package(OpenGL REQUIRED)
    target_include_directories(sdl.hdll
        PRIVATE
        ${OPENGL_INCLUDE_DIR}
    )
    target_link_libraries(sdl.hdll
        libhl
        ${OPENGL_gl_LIBRARY}
    )
endif()


install(
    TARGETS sdl.hdll
    DESTINATION ${HDLL_DESTINATION}
)
