OV7670 driver, based on [Adafruit CircuitPython OV7670 Library](https://github.com/adafruit/Adafruit_CircuitPython_OV7670/)

## Usage
Add *ov7670* into CMakeLists.txt, in `target_link_libraries`

### Pin mapping
## OV7670 Pin Mapping (Raspberry Pi Pico)

| Signal (name)          | GPIO | Function / usage                       | Direction (RP2350) | Observações |
|-----------------------|------|------------------------------------|------------------|-------------|
| `OV7670_MCLK_PIN`     | 20   | MCLK (master clock, PWM)           | output (PWM)      | Frequency defined by `OV7670_MCLK_FREQUENCY` (MHz). |
| `OV7670_RESET_PIN`    | 10   | RESET do módulo OV7670             | output            | Drives the camera reset pin. |
| `OV7670_PCLK_PIN`     | 11   | PCLK (pixel clock da câmera)       | input          | Synchronizes reading of the 8-bit data bus. |
| `OV7670_HREF_PIN`     | 21   | HREF (start/end de linha)          | input          | Valid pixel data for each line. |
| `OV7670_VSYNC_PIN`    | 7    | VSYNC (start/end de frame)         | input          | Synchronizes the start and end of a frame. |
| `OV7670_PWDN_PIN`     | -1   | PWDN (power down) — **not used**  | —                | `-1` = Power-down pin (PWDN). Controls camera power on/off. Not connected by default. |
| `_OV7670_I2C_SDA_PIN` | 8    | I²C SDA (SCCB)                     | SDA (I²C)        | Must be set with `GPIO_FUNC_I2C` + pull-up. |
| `_OV7670_I2C_SCL_PIN` | 9    | I²C SCL (SCCB)                     | SCL (I²C)        | Must be set with `GPIO_FUNC_I2C` + pull-up. |
| `OV7670_DATA_PINS[0]` | 12   | Data bit 0 (LSB)                   | input          | Parallel data bus `{12..19}`. |
| `OV7670_DATA_PINS[1]` | 13   | Data bit 1                         | input          | — |
| `OV7670_DATA_PINS[2]` | 14   | Data bit 2                         | input          | — |
| `OV7670_DATA_PINS[3]` | 15   | Data bit 3                         | input          | — |
| `OV7670_DATA_PINS[4]` | 16   | Data bit 4                         | input          | — |
| `OV7670_DATA_PINS[5]` | 17   | Data bit 5                         | input          | — |
| `OV7670_DATA_PINS[6]` | 18   | Data bit 6                         | input          | — |
| `OV7670_DATA_PINS[7]` | 19   | Data bit 7 (MSB)                   | input          | — |

### Notes
- MCLK (GPIO 20) is generated through PWM, configured with the default 16MHz.  
- I²C (GPIO 8=SDA, GPIO 9=SCL) uses a `i2c0` at 100 kHz. Must use external pull-up 4.7kOhm resistors.  
- This version uses polling to retrieve data from the camera.



### Functions:

| Function | Description |
|----------|-------------|
| `ov7670_config(void);` | Configures pins, including MCLK, I²C, RESET and initializes the camera |
| `ov7670_capture(uint8_t *buf, size_t len, int width, int height);` | Captures a frame from the camera and stores it into a buffer |
| `ov7670_write_register(uint8_t reg, uint8_t val);` | Writes a value to an OV7670 register using I²C |
| `ov7670_read_register(uint8_t reg);` | Reads a register’s value from OV7670 using I²C |
| `ov7670_register_writelist(void);` | Writes a predefined list of registers and values to the camera |
| `ov7670_register_test(void);` | Checks camera Product ID and Version Number |
| `ov7670_product_id(void);` | Returns the camera Product ID |
| `ov7670_product_version(void);` | Returns the camera Product Version |
| `ov7670_pins_config(void);` | Configures and initializes DATA, VSYNC, HREF and PCLK pins |
| `ov7670_mclk_config(void);` | Generates an MCLK using PWM |
| `ov7670_i2c_config(void);` | Initializes I²C for use with SCCB protocol |
| `ov7670_reset(void);` | Applies a hardware reset to the camera through RESET pin |
| `ov7670_shutdown(void);` | Controls the PWDN pin to power on/off the camera |
| `oov7670_frame_control(uint8_t size, uint16_t vstart, uint16_t hstart, uint8_t edge_offset, uint8_t pclk_delay);` | Adjusts parameters related to scaling, window size, and clock for different resolutions |

