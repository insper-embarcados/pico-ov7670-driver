#include <stdio.h>
#include "pico/stdlib.h"
#include "ov7670.h"
#include <string.h>

// observations:
// use 4.7Kohm pullups on SDA and SCL lines

int main()
{


    
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
    int size = OV7670_SIZE_DIV4; // 160x120
    WIDTH = 160;
    HEIGHT = 120;
    ov7670_frame_control(size, _window[size][0],_window[size][1] , _window[size][2], _window[size][3]);


    // Configuração da câmera
    
    uint8_t buf[WIDTH * HEIGHT];  // só Y (1 byte por pixel)

    
    while (true) {
        int n = ov7670_capture(buf, sizeof(buf), WIDTH, HEIGHT);

        // envia marcador de início
        printf("FRAME\n");

        // envia os bytes crus
        fwrite(buf, 1, n, stdout);

        sleep_ms(50); // intervalo entre frames
    }

}
