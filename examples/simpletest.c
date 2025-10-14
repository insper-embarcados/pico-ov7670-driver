#include <stdint.h>
#include <stdio.h>
#include "ov7670.h"
#include "pico/stdlib.h"


// observations:
// use 4.7Kohm pullups on SDA and SCL lines

const char ascii_map[] = " .:-=+*#%@";

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
  int size = OV7670_SIZE_DIV8; // 160x120
  WIDTH = 80;
  HEIGHT = 60;
  ov7670_frame_control(size, _window[size][0], _window[size][1],
                       _window[size][2], _window[size][3]);

  uint8_t buf[WIDTH * HEIGHT];
  sleep_ms(1000);


// pra teste

//   while (true) {
//     int n = ov7670_capture(buf, sizeof(buf), WIDTH, HEIGHT);
//     // printf("Captured %d bytes\n", n);
//     for (int y = 0; y < HEIGHT; y++) {
//       for (int x = 0; x < WIDTH; x++) {
//         uint8_t Y = buf[y * WIDTH + x];
//         int level = (Y * (sizeof(ascii_map) - 2)) / 255;
//         putchar(ascii_map[level]);
//       }
//       putchar('\n');
//     }
//   }
// }


// pra treino

while (true) {
    int n = ov7670_capture(buf, sizeof(buf), WIDTH, HEIGHT);
    // printf("Captured %d bytes\n", n);
    printf("frame start:[");
    for (int y = 0; y < HEIGHT; y++) {
      for (int x = 0; x < WIDTH; x++) {
        uint8_t Y = buf[y * WIDTH + x];
        int level = (Y * (sizeof(ascii_map) - 2)) / 255;
        printf("%d ,", Y);

      }
    }
    printf("]frame finish\n");

  }
}


