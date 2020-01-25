#created by Sin(an)

import sensor, image, uart

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)

threshold_blobs = [(29, 0, -34, -3, -26, 9)]
threshold_line = [(1, 1, 1, 1, 1 ,1)]

roi_blobs = [0, 180, 320, 60]

height = sensor.height()
width = sensor.width()
message = 0

while(True):
    img = sensor.snapshot()
    blobs = img.find_blobs(threshold_blobs, False, roi_blobs)
    if len(blobs) > 0:
        comunication(5)
    for blob in blobs:
        if len(blobs) == 1:
            roi_left = [0, blob.y(), blob.x(), blob.y() + blob.h()]
            roi_right = [blob.x(), blob.y(), width, blob.y() + blob.h()]
            roi_top = [blob.x(), 0, blob.x() + blob.w(), blob.y()]

            upper_line = img.find_blobs(threshold_line, False, roi_top)
            left_line = img.find_blobs(trheshold_line, False, roi_left)
            right_line = img.find_blobs(trheshold_line, False, roi_right)

            if len(upper_line) != 0:
                if len(left_line) != 0:
                    message = 2
                elif len(right_line) !=:
                    message = 1
        elif len(blobs) == 2:
            first_blob = blob[0]
            roi_left_1 = [0, first_blob.y(), first_blob.x(), first_blob.y() + first_blob.h()]
            roi_right_1 = [first_blob.x(), first_blob.y(), width, first_blob.y() + first_blob.h()]
            roi_top_1 = [first_blob.x(), 0, first_blob.x() + first_blob.w(), first_blob.y()]

            second_blob = blob[1]
            roi_left_2 = [0, second_blob.y(), second_blob.x(), second_blob.y() + second_blob.h()]
            roi_right_2 = [second_blob.x(), second_blob.y(), width, second_blob.y() + second_blob.h()]
            roi_top_2 = [second_blob.x(), 0, second_blob.x() + second_blob.w(), second_blob.y()]

            upper_line_1 = img.find_blobs(threshold_line, False, roi_top_1)
            left_line_1 = img.find_blobs(trheshold_line, False, roi_left_1)
            right_line_1 = img.find_blobs(trheshold_line, False, roi_right_1)

            upper_line_2 = img.find_blobs(threshold_line, False, roi_top_2)
            left_line_2 = img.find_blobs(trheshold_line, False, roi_left_2)
            right_line_2 = img.find_blobs(trheshold_line, False, roi_right_2)

            if len(upper_line_1) != 0:
                if len(upper_line_2) != 0:
                    message = 3
                elif len(upper_line_2) == 0:
                    if len(left_line_1) != 0:
                        message = 2
                    elif len(right_line_1) != 0:
                        message = 1
            elif len(upper_line_1) == 0:
                if len(upper_line_2) != 0:
                    if len(left_line_2) != 0:
                        message = 2
                    if len(right_line_2) != 0:
                        message = 1
            elif len(blobs) == 3:
                first_blob = blob[0]
                second_blob = blob[1]
                third_blob = blob[2]

                yVals = [first_blob.y(), second_blob.y(), third_blob.y()]
                highestY = yVals.index(min(yVals))
                rel_blob = yVals[highestY]

                roi_left = [0, rel_blob.y(), rel_blob.x(), rel_blob.y() + rel_blob.h()]
                roi_right = [rel_blob.x(), rel_blob.y(), width, rel_blob.y() + rel_blob.h()]
                roi_top = [rel_blob.x(), 0, rel_blob.x() + rel_blob.w(), rel_blob.y()]

                upper_line = img.find_blobs(threshold_line, False, roi_top)
                left_line = img.find_blobs(trheshold_line, False, roi_left)
                right_line = img.find_blobs(trheshold_line, False, roi_right)

                if len(upper_line) != 0:
                    if len(left_line) != 0:
                        message = 2
                    elif len(right_line) != 0:
                        message = 1

            elif len(blobs) == 4:
                message = 3

    def communitcation(messageToSend):
        uart.write("%d"%messageToSend + "\n")

"""
uart table:
0 = foreward
1 = left
2 = right
3 = trun around
5 = blob detected
"""
