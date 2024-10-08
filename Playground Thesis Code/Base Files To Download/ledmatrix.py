import time

I2C_CMD_CONTINUE_DATA = 0x81

GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR = 0x65  # Default I2C address
GROVE_TWO_RGB_LED_MATRIX_VID = 0x2886         # Vendor ID
GROVE_TWO_RGB_LED_MATRIX_PID = 0x8005         # Product ID

I2C_CMD_GET_DEV_ID = 0x00
I2C_CMD_DISP_BAR = 0x01
I2C_CMD_DISP_EMOJI = 0x02
I2C_CMD_DISP_NUM = 0x03
I2C_CMD_DISP_STR = 0x04
I2C_CMD_DISP_CUSTOM = 0x05
I2C_CMD_DISP_OFF = 0x06
# I2C_CMD_DISP_ASCII is not used
I2C_CMD_DISP_FLASH = 0x08
I2C_CMD_DISP_COLOR_BAR = 0x09
I2C_CMD_DISP_COLOR_WAVE = 0x0A
I2C_CMD_DISP_COLOR_CLOCKWISE = 0x0B
I2C_CMD_DISP_COLOR_ANIMATION = 0x0C
I2C_CMD_DISP_COLOR_BLOCK = 0x0D

I2C_CMD_STORE_FLASH = 0xA0
I2C_CMD_DELETE_FLASH = 0xA1

I2C_CMD_LED_ON = 0xB0
I2C_CMD_LED_OFF = 0xB1
I2C_CMD_AUTO_SLEEP_ON = 0xB2
I2C_CMD_AUTO_SLEEP_OFF = 0xB3

I2C_CMD_DISP_ROTATE = 0xB4
I2C_CMD_DISP_OFFSET = 0xB5

I2C_CMD_SET_ADDR = 0xC0
I2C_CMD_RST_ADDR = 0xC1

I2C_CMD_TEST_TX_RX_ON = 0xE0
I2C_CMD_TEST_TX_RX_OFF = 0xE1
I2C_CMD_TEST_GET_VER = 0xE2

I2C_CMD_GET_DEVICE_UID = 0xF1


class LEDMATRIX:
    def __init__(self, i2c, base_address=GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR, offset_address=0):
        self.i2c = i2c
        self.base_address = base_address
        self.offset_address = offset_address
        self.current_device_address = base_address + offset_address

    def _i2c_send_byte(self, address, data):
        self.i2c.writeto(address, bytearray([data]))

    def _i2c_send_bytes(self, address, data):
        self.i2c.writeto(address, bytearray(data))

    def _i2c_receive_bytes(self, address, length):
        return self.i2c.readfrom(address, length)

    def get_device_vid(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_GET_DEV_ID)
        data = self._i2c_receive_bytes(self.current_device_address, 4)
        return data[0] + (data[1] << 8)

    def get_device_pid(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_GET_DEV_ID)
        data = self._i2c_receive_bytes(self.current_device_address, 4)
        return data[2] + (data[3] << 8)

    def change_device_base_address(self, new_address):
        if not (0x10 <= new_address <= 0x70):
            new_address = GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR

        data = [I2C_CMD_SET_ADDR, new_address]
        self._i2c_send_bytes(self.current_device_address, data)
        self.base_address = new_address
        self.current_device_address = self.base_address + self.offset_address
        time.sleep_ms(200)

    def default_device_address(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_RST_ADDR)
        self.base_address = GROVE_TWO_RGB_LED_MATRIX_DEF_I2C_ADDR
        self.current_device_address = self.base_address + self.offset_address
        time.sleep_ms(200)

    def turn_on_led_flash(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_LED_ON)

    def turn_off_led_flash(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_LED_OFF)

    def enable_auto_sleep(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_AUTO_SLEEP_ON)

    def wake_device(self):
        sleep_us(200)

    def disable_auto_sleep(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_AUTO_SLEEP_OFF)

    def set_display_orientation(self, orientation):
        data = [I2C_CMD_DISP_ROTATE, orientation]
        self._i2c_send_bytes(self.current_device_address, data)

    def set_display_offset(self, offset_x, offset_y):
        offset_x = max(0, min(16, offset_x + 8))
        offset_y = max(0, min(16, offset_y + 8))
        data = [I2C_CMD_DISP_OFFSET, offset_x, offset_y]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_bar(self, bar, duration_time, forever_flag, color):
        if bar > 32:
            bar = 32
        data = [I2C_CMD_DISP_BAR, bar, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag, color]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_emoji(self, emoji, duration_time, forever_flag):
        data = [I2C_CMD_DISP_EMOJI, emoji, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_number(self, number, duration_time, forever_flag, color):
        data = [I2C_CMD_DISP_NUM, number & 0xff, (number >> 8) & 0xff, duration_time & 0xff,
                (duration_time >> 8) & 0xff, forever_flag, color]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_string(self, text, duration_time, forever_flag, color):
        text = text[:28]  # Max length is 28
        length = len(text)
        data = [I2C_CMD_DISP_STR, forever_flag, duration_time & 0xff, (duration_time >> 8) & 0xff, length, color] + \
               list(map(ord, text))
        if length > 25:
            self._i2c_send_bytes(self.current_device_address, data[:31])
            time.sleep_ms(1)
            self._i2c_send_bytes(self.current_device_address, data[31:])
        else:
            self._i2c_send_bytes(self.current_device_address, data)

    def display_frames(self, buffer, duration_time, forever_flag, frames_number):
        if frames_number > 5:
            frames_number = 5
        if frames_number == 0:
            return
        for i in range(frames_number - 1, -1, -1):
            data = [I2C_CMD_DISP_CUSTOM, 0, 0, 0, frames_number, i] + buffer[i * 64: (i + 1) * 64]
            if i == 0:
                data[1] = duration_time & 0xff
                data[2] = (duration_time >> 8) & 0xff
                data[3] = forever_flag
            self._i2c_send_bytes(self.current_device_address, data[:24])
            time.sleep_ms(1)
            self._i2c_send_bytes(self.current_device_address, data[24:48])
            time.sleep_ms(1)
            self._i2c_send_bytes(self.current_device_address, data[48:72])

    def stop_display(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_DISP_OFF)

    def store_frames(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_STORE_FLASH)
        time.sleep_ms(200)

    def delete_frames(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_DELETE_FLASH)
        time.sleep_ms(200)

    def display_frames_from_flash(self, duration_time, forever_flag):
        data = [I2C_CMD_DISP_FLASH, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_color_block(self, color):
        data = [I2C_CMD_DISP_COLOR_BLOCK, color]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_color_bar(self, duration_time, forever_flag):
        data = [I2C_CMD_DISP_COLOR_BAR, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_color_wave(self, duration_time, forever_flag):
        data = [I2C_CMD_DISP_COLOR_WAVE, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_clockwise(self, duration_time, forever_flag):
        data = [I2C_CMD_DISP_COLOR_CLOCKWISE, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def display_color_animation(self, index, duration_time, forever_flag):
        data = [I2C_CMD_DISP_COLOR_ANIMATION, index, duration_time & 0xff, (duration_time >> 8) & 0xff, forever_flag]
        self._i2c_send_bytes(self.current_device_address, data)

    def enable_test_mode(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_TEST_TX_RX_ON)

    def disable_test_mode(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_TEST_TX_RX_OFF)

    def get_test_version(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_TEST_GET_VER)
        return self._i2c_receive_bytes(self.current_device_address, 3)

    def get_device_uid(self):
        self._i2c_send_byte(self.current_device_address, I2C_CMD_GET_DEVICE_UID)
        return self._i2c_receive_bytes(self.current_device_address, 4)