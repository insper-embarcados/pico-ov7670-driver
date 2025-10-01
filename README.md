# Pico C SDK OV7670 Library

Pico C SDK Driver for 0V7670 cameras raspberry pi Pico 1 and 2.


## Dependencies

The driver needs:
- Pico C SDK
- Raspberry Pi Pico (RP2040 or 2350)


## Usage Example


Inside `examples/` folder we have two diffent examples, both using Y (from YUV):
- simplestest: an example that reproduces the camera image as ASCII art over UART.
- selfietest: an example that uses an ili9341 display to reproduce the image.
To compile a specific example, follow the instructions in [add_executable](https://github.com/danielmpinto/pico-ov7670-driver/blob/main/CMakeLists.txt)

### Selfie camera example using ili9341 320x240 pixels and OV7670 camera:

```c
#include <stdio.h>
#include "pico/stdlib.h"
#include "ov7670.h"
#include "ili9341.h"
#include "gfx.h"
#include "touch_resistive.h"

// observations:
// use 4.7Kohm pullups on SDA and SCL lines

static inline uint16_t Y_to_gray565(uint8_t Y) {
    return GFX_RGB565(Y, Y, Y);
}

void draw_frame(uint8_t *buf, int width, int height) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            uint8_t Y = buf[y * width + x];
            uint16_t color = Y_to_gray565(Y);
            GFX_drawPixel(x, y, color);
        }
    }
    GFX_flush();  /// send to display
}


int main()
{
    stdio_init_all();
    ov7670_shutdown();
    ov7670_config();

    int size = OV7670_SIZE_DIV2; // 320x240
    WIDTH = 320;
    HEIGHT = 240;
    ov7670_frame_control(size, _window[size][0],_window[size][1] , _window[size][2], _window[size][3]);
    
    uint8_t buf[WIDTH * HEIGHT];  
    stdio_init_all();         

    LCD_initDisplay();        
    LCD_setRotation(1);       
    GFX_createFramebuf();     
    configure_touch();        

    while (true) {
        ov7670_capture(buf, sizeof(buf), WIDTH, HEIGHT);
        draw_frame(buf, WIDTH, HEIGHT);
    }

}
```

### Output of the example

Mouser Eletronics doll:

![Output2 ](/imgs/output2.jpeg "Output 2")


## Schematic

Please, see the camera pins table [here](https://github.com/danielmpinto/pico-ov7670-driver/tree/main/lib_ov7670).
If you need to check the `lib_ili9341/` pins, look at the files in the lib_ili9341 folder.


My setup for testing:

![Setup ](/imgs/setup.jpeg "Setup")


## References
This driver is an adaptation of the [CircuitPython driver for OV7670 cameras](https://github.com/adafruit/Adafruit_CircuitPython_OV7670/).


