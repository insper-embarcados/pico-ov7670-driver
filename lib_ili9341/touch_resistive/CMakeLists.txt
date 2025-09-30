add_library(touch_resistive
        touch_resistive.c touch_resistive.h
        )

target_include_directories(touch_resistive PUBLIC
	${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(touch_resistive pico_stdlib ili9341 gfx hardware_adc)



