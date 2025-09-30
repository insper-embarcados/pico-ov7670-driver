# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico2 CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico2_camera C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(pico2_camera 

                # compiles simpletest
                simpletest.c 
                
                # compile selfie test

                # GFX / ILI9341 / TOUCH
                # tft_lcd_ili9341/gfx/gfx.c
                # tft_lcd_ili9341/ili9341/ili9341.c
                # tft_lcd_ili9341/touch_resistive/touch_resistive.c)
)
pico_set_program_name(pico2_camera "pico2_camera")
pico_set_program_version(pico2_camera "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(pico2_camera 1)
pico_enable_stdio_usb(pico2_camera 0)




# Add the standard library to the build
target_link_libraries(pico2_camera
        pico_stdlib
        ov7670
        hardware_spi
        hardware_dma
        hardware_adc
        )



# Add the standard include files to the build
target_include_directories(pico2_camera PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
)

add_subdirectory(ov7670)

pico_add_extra_outputs(pico2_camera)

