#created by Sin(an)
#Version 4.0

import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)
pin = pyb.Pin("P7", pyb.Pin.OUT_PP)

width = sensor.width()
height = sensor.height()
threshold_blobs = [(16, 57, -128, -18, -128, 127)]
threshold_line = [(0, 27, -10, 38, -128, 127)]
threshold_circle = [(0, 16, -128, 127, -128, 127)]
threshold_zone = [(0, 31, -128, 127, -128, 127)]
roi_blobs_stop = [0, 150, width, 90]
roi_circles = [0, 0, int(width/2), height]
blobs_y = []
message = 0
circle_area = 100
zone_area = 12000
min_r = 20
max_r = 40

def communication(messageToSend):
    print(messageToSend)
    uart.write("%d"%messageToSend)

def incomingByte():
    if uart.any() != 0:
        income = uart.readchar()
    else:
        income = 0
    if income != 0:
        print(income)
    return income

def main():
    global message
    img = sensor.snapshot()
    blobs_stop = img.find_blobs(threshold_blobs, False, roi_blobs_stop, merge=True, x_stride=10, y_stride=10, area_threshold=900)

    if len(blobs_stop) != 0:
        communication(5)
        for blob in blobs_stop:
            blobs_y.append(blob.y())
        high_y = max(blobs_y)
        print(blobs_y)
        roi_blobs = [0, high_y, width, height-high_y]
        img.draw_rectangle(roi_blobs_stop, 700)
        img.draw_rectangle(roi_blobs)
        rel_blobs = img.find_blobs(threshold_blobs, False, roi_blobs, merge=True, x_stride=10, y_stride=10, area_threshold=900)

        if len(rel_blobs) == 1:
            blob = rel_blobs[0]
            roi_right = [blob.x()+blob.w(), blob.y(), width-(blob.x()+blob.w()), blob.h()]
            roi_left = [0, blob.y(), blob.x(), blob.h()]
            roi_bottom = [blob.x(), blob.y()+blob.h(), blob.w(), height-(blob.y()+blob.h())]

            left_line = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
            right_line = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)
            bottom_line = img.find_blobs(threshold_line, False, roi_bottom, area_threshold=900)
            if len(left_line) != 0:
                message = 2 #right
            elif len(right_line) != 0:
                message = 1 #left
            if len(bottom_line) != 0:
                message = 0

        elif len(rel_blobs) == 2:
            blob_1 = rel_blobs[0]
            blob_2 = rel_blobs[1]

            roi_bottom_1 = [blob_1.x(), blob_1.y()+blob_1.h(), blob_1.w(), height-(blob_1.y()+blob_1.h())]
            roi_bottom_2 = [blob_2.x(), blob_2.y()+blob_2.h(), blob_2.w(), height-(blob_2.y()+blob_2.h())]

            bottom_line_1 = img.find_blobs(threshold_line, False, roi_bottom_1, area_threshold=900)
            bottom_line_2 = img.find_blobs(threshold_line, False, roi_bottom_2, area_threshold=900)

            if len(bottom_line_1) != 0:
                if len(bottom_line_2) != 0:
                    message = 0
            else:
                message = 3

        blobs_y.clear()
        communication(message)

def isBlack():
    sensor.set_pixformat(sensor.RGB565)
    sensor.skip_frames(10)
    img = sensor.snapshot()
    black = img.find_blobs(threshold_circle, area_threshold=circle_area-500)
    if len(black) != 0:
        print("Black")

def circles():
    global circle_area
    pyb.LED(1).on()
    sensor.set_pixformat(sensor.GRAYSCALE)
    sensor.set_framesize(sensor.QQVGA)
    img = sensor.snapshot()
    circles = img.find_circles(roi_circles, threshold=1800, x_margin=70, y_margin=70, r_margin=70, r_min=min_r, r_max=max_r)
    for circle in circles:
        circle_area = (2 * circles[0].r()) * (2 * circles[0].r())
    if len(circles) != 0:
        communication(1)
        isBlack()
    else:
        communication(0)
    zone()

def zone():
    img = sensor.snapshot()
    black = img.find_blobs(threshold_zone, area_threshold=zone_area)
    if len(black) != 0:
        communication(6)

def lobby():
    pyb.LED(3).on()
    if incomingByte() == 7:
        while(1):
            circles()
    else:
        main()

def setup():
    pin.high()
    while(1):
        lobby()

setup()
"""
uart table:
0 = foreward
1 = left
2 = right
3 = trun around
5 = blob detected
7 = last room
9 = drive back
"""
