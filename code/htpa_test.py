import lcd
import image
import time
#import sensor
from modules import htpa
from machine import I2C


# i2c = I2C(I2C.I2C0, freq=100000, scl=7, sda=6)
lcd.init()
lcd_w = 320
lcd_h = 240

edge = (-1, -1, -1, -1, 8, -1, -1, -1, -1)

offset_x = 0
offset_y = 50
zoom = 2
rotate = 0

lcd.init(type=2, freq=20000000)
lcd.rotation(1)
dev = htpa(i2c=I2C.I2C0, scl_pin=7, sda_pin=6, i2c_freq=1000000)
sensor_width = dev.width()
sensor_height = dev.height()
img = image.Image(size=(32, 32))
# img = img.to_grayscale()
# clock = time.clock()
while 1:
    # clock.tick()
    try:
        temperature = dev.temperature()

        min, max, min_pos, max_pos = dev.min_max()
        temp_range = max - min + 1
        img = dev.to_image(min, max)
        img = img.rotation_corr(z_rotation=90)
        img = img.replace(img, hmirror=True)
        max_temp_pos = (max_pos//sensor_width, max_pos % sensor_width)
        img = img.resize(lcd_w, lcd_h)
        img = img.to_rainbow(1)

        # max
        max_temp_pos = (
            int(lcd_w/sensor_width*max_temp_pos[0]),
            int(lcd_h/sensor_height*max_temp_pos[1])
        )

        if max_temp_pos[0] >= lcd_w/2:
            x = max_temp_pos[0] - 80
        else:
            x = max_temp_pos[0] + 4
        print((max/100.0))
        img = img.draw_rectangle(
            x, max_temp_pos[1], 80, 22, color=(0xff, 112, 0xff), fill=True)
        img = img.draw_string(x, max_temp_pos[1], "%.2f" % (
            max/100.0), color=(0xff, 0xff, 0xff), scale=2)
        img = img.draw_cross(max_temp_pos[0], max_temp_pos[1], color=(
            0xff, 0xff, 0xff), thickness=3)
        lcd.display(img)
        del img
        # print(clock.fps())
    except Exception as e:
        print(e)
