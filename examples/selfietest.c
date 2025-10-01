#include <stdio.h>
#include "pico/stdlib.h"
#include "gfx.h"
#include "ili9341.h"
#include "ov7670.h"
#include "touch_resistive.h"

// observations:
// use 4.7Kohm pullups on SDA and SCL lines

static inline uint16_t Y_to_gray565(uint8_t Y) {
  // turn Y (0-255) into a gray color in RGB565 format
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
  GFX_flush(); /// send to display
}

int main() {

  stdio_init_all();
  // ov7670 shutdown, theorically not needed
  ov7670_shutdown();
  ov7670_config();

  // defines size
  // OV7670_SIZE_DIV1            0  //"""640 x 480"""
  // OV7670_SIZE_DIV2            1  //"""320 x 240"""
  // OV7670_SIZE_DIV4            2  //"""160 x 120"""
  // OV7670_SIZE_DIV8            3  //"""80 x 60"""
  // OV7670_SIZE_DIV16           4  //"""40 x 30"""
  int size = OV7670_SIZE_DIV2; // 320x240
  WIDTH = 320;
  HEIGHT = 240;
  ov7670_frame_control(size, _window[size][0], _window[size][1],
                       _window[size][2], _window[size][3]);

  uint8_t buf[WIDTH * HEIGHT];
  stdio_init_all();

  // inilitializations display and touch
  LCD_initDisplay();
  LCD_setRotation(1);
  GFX_createFramebuf();
  configure_touch();

  while (true) {
    // sends to display
    // creating a image of 160x120 pixels

    ov7670_capture(buf, sizeof(buf), WIDTH, HEIGHT);
    draw_frame(buf, WIDTH, HEIGHT);
  }
}
