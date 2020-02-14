# Untitled - By: Test - Di Feb 11 2020

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
width = sensor.width()
height = sensor.height()
clock = time.clock()
roi_circle = [0, 0, width/2, height]
min_r = 20
max_r = 40
while(True):
    clock.tick()
    img = sensor.snapshot()
    circles = img.find_circles(roi, threshold=1800, x_margin=70, y_margin=70, r_margin=70, r_min=min_r, r_max=max_r)
    if len(circles) != 0:
        print(1)
