add_library(ili9341 ili9341.c ili9341.h
)

target_include_directories(ili9341 PUBLIC
	${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(ili9341 pico_stdlib hardware_spi hardware_dma)