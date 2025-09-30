# add_library(ov7670 ov7670.c)

# add_executable(ov7670
#                 ov7670.c)


add_library(ov7670 ov7670.c ov7670.h)

target_include_directories(ov7670 PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(ov7670 pico_stdlib hardware_i2c hardware_pwm hardware_clocks)

