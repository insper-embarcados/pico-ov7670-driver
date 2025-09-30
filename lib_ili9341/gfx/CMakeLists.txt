add_library(gfx
	gfx.c gfx.h
)

target_include_directories(gfx PUBLIC
	${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(gfx pico_stdlib hardware_dma ili9341)