import sensor
import image
import lcd
import time
import KPU as kpu


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)

lcd.clear()
# lcd.draw_string(100, 96, "MobileNet Demo")
# lcd.draw_string(100, 112, "Loading labels...")
with open('labels.txt', 'r') as f:
    labels = f.readlines()

task = kpu.load(0x200000)
clock = time.clock()

while True:
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    # fps = clock.fps()
    plist = fmap[:]
    pmax = max(plist)
    max_index = plist.index(pmax)
    a = lcd.display(img, oft=(0, 0))
    lcd.draw_string(0, 224, "%.2f:%s" % (pmax, labels[max_index].strip()))
    # print(fps)

a = kpu.deinit(task)
