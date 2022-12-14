import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
import touchscreen as ts
from machine import Timer, I2C


i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
lcd.init()
#lcd.rotation(1)
lv.init()

ts.init(i2c, cal=(78, -5669, 21013658, 4010, 1, -449360, 65536))
#ts.init(i2c)
#fixed = ts.calibrate()
#print(fixed)

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
disp_drv.hor_res = 320
disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

indev_drv = lv.indev_drv_t()
lv.indev_drv_init(indev_drv)
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = lv_h.read
lv.indev_drv_register(indev_drv)

# lv.log_register_print_cb(lv_h.log)
# lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))

scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_size(10, 10)
label.set_text("Start")
lv.scr_load(scr)

def on_timer(timer):
    lv.tick_inc(5)

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
    tim = time.ticks_ms()
    lv.task_handler()
    while time.ticks_ms()-tim < 5:
        pass
