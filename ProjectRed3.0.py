#created by Sin(an)
#Version 3.5

import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)

height = sensor.height()
width = sensor.width()

threshold_blobs = [(57, 8, -9, -128, -128, 127)]
threshold_line = [(57, 8, -2, 127, -128, 117)]

roi_blobs_stop = [0, 180, width, 60]
roi_screen = [0, 0, width, height]

message = 0
while(True):
    pyb.LED(1).on()
    pyb.LED(2).on()

    def communication(messageToSend):
        print(messageToSend)
        uart.write("%d"%messageToSend)

    def main():
        global message
        img = sensor.snapshot()
        blobs_stop = img.find_blobs(threshold_blobs, False, roi_blobs_stop, merge=True, x_stride=10, y_stride=10, area_threshold=900)
        blobs = img.find_blobs(threshold_blobs, False, roi_screen, merge=True, x_stride=10, y_stride=10, area_threshold=900)
        if len(blobs_stop) > 0:
            communication(5)
            for blob in blobs:
                if len(blobs) == 1:
                    roi_left = [0, blob.y(), blob.x(), blob.h()]
                    roi_right = [blob.x(), blob.y(), width - blob.x(), blob.h()]
                    roi_top = [blob.x(), 0, blob.w(), blob.y()]
                    roi_bottom = [blob.x(), blob.y(), blob.w(), height-blob.y()]
                    img.draw_rectangle(roi_left, 900)
                    img.draw_rectangle(roi_right, 300)
                    img.draw_rectangle(roi_top, 50)
                    if blob.h() != 0:
                        try:
                            upper_line = img.find_blobs(threshold_line, False, roi_top, area_threshold=900)
                            left_line = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
                            right_line = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)
                            lower_line = img.find_blobs(threshold_line, False, roi_bottom, area_threshold=1500)
                        except:
                            break

                        if len(upper_line) != 0:
                            if len(left_line) != 0:
                                message = 2
                            elif len(right_line) != 0:
                                message = 1
                        if len(lower_line) != 0:
                            message = 0
                elif len(blobs) == 2:
                    first_blob = blobs[0]
                    roi_left_1 = [0, first_blob.y(), first_blob.x(), first_blob.h()]
                    roi_right_1 = [first_blob.x(), first_blob.y(), width, first_blob.h()]
                    roi_top_1 = [first_blob.x(), 0, first_blob.w(), first_blob.y()]

                    second_blob = blobs[1]
                    roi_left_2 = [0, second_blob.y(), second_blob.x(), second_blob.h()]
                    roi_right_2 = [second_blob.x(), second_blob.y(), width, second_blob.h()]
                    roi_top_2 = [second_blob.x(), 0, second_blob.w(), second_blob.y()]

                    if first_blob.h() != 0:
                        try:
                            upper_line_1 = img.find_blobs(threshold_line, False, roi_top_1, area_threshold=900)
                            left_line_1 = img.find_blobs(threshold_line, False, roi_left_1, area_threshold=900)
                            right_line_1 = img.find_blobs(threshold_line, False, roi_right_1, area_threshold=900)
                            upper_line_2 = img.find_blobs(threshold_line, False, roi_top_2, area_threshold=900)
                            left_line_2 = img.find_blobs(threshold_line, False, roi_left_2, area_threshold=900)
                            right_line_2 = img.find_blobs(threshold_line, False, roi_right_2, area_threshold=900)
                        except:
                            break
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
                        roi_left =  [0, 0, 30, height]
                        roi_right = [290, 0, 30, height]

                        line_left = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
                        line_right = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)
                        if line_left and line_right:
                        #horizontal_line = img.draw_line(line_left.cx(), line_left.cy(), line_right.cx(), line_right.cy())
                            horizontal_val = int((line_left[0].cy() + line_right[0].cx()) / 2)
                            roi_blobs = [0, horizontal_val, width, horizontal_val]

                            blobs_by3 = img.find_blobs(threshold_blobs, False, roi_blobs, area_threshold=900)

                            if len(blobs_by3) == 2:
                                message = 3

                            elif len(blobs_by3) == 1:
                                blob = blobs_by3[0]

                                roi_left = [0, blob.y(), blob.x(), blob.h()]
                                roi_right = [blob.x(), blob.y(), width - blob.x(), blob.h()]
                                roi_top = [blob.x(), 0, blob.w(), blob.y()]

                                upper_line = img.find_blobs(threshold_line, False, roi_top, area_threshold=900)
                                left_line = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
                                right_line = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)

                                if len(upper_line) != 0:
                                    if len(left_line) != 0:
                                        message = 2
                                    elif len(right_line) != 0:
                                        message = 1
                        """
                        first_blob = blobs[0]
                        second_blob = blobs[1]
                        third_blob = blobs[2]
                        img.draw_rectangle(first_blob.rect())
                        img.draw_rectangle(second_blob.rect())
                        img.draw_rectangle(third_blob.rect())

                        roi_left_1 = [0, first_blob.y(), first_blob.x(), first_blob.h()]
                        roi_right_1 = [first_blob.x(), first_blob.y(), width, first_blob.h()]
                        roi_top_1 = [first_blob.x(), 0, first_blob.w(), first_blob.y()]

                        roi_left_2 = [0, second_blob.y(), second_blob.x(), second_blob.h()]
                        roi_right_2 = [second_blob.x(), second_blob.y(), width, second_blob.h()]
                        roi_top_2 = [second_blob.x(), 0, second_blob.w(), second_blob.y()]

                        roi_left_3 = [0, third_blob.y(), third_blob.x(), third_blob.h()]
                        roi_right_3 = [third_blob.x(), third_blob.y(), width, third_blob.h()]
                        roi_top_3 = [third_blob.x(), 0, third_blob.w(), third_blob.y()]
                        img.draw_rectangle(roi_top_1)
                        if first_blob.y() != 0:
                            upper_line_1 = img.find_blobs(threshold_line, False, roi_top_1, area_threshold=900)
                            left_line_1 = img.find_blobs(threshold_line, False, roi_left_1, area_threshold=900)
                            right_line_1 = img.find_blobs(threshold_line, False, roi_right_1, area_threshold=900)

                            upper_line_2 = img.find_blobs(threshold_line, False, roi_top_2, area_threshold=900)
                            left_line_2 = img.find_blobs(threshold_line, False, roi_left_2, area_threshold=900)
                            right_line_2 = img.find_blobs(threshold_line, False, roi_right_2, area_threshold=900)

                            upper_line_3 = img.find_blobs(threshold_line, False, roi_top_3, area_threshold=900)
                            left_line_3 = img.find_blobs(threshold_line, False, roi_left_3, area_threshold=900)
                            right_line_3 = img.find_blobs(threshold_line, False, roi_right_3, area_threshold=900)

                            rel_dots = []
                            if len(upper_line_1) > 0:
                                rel_dots.append(first_blob)
                            if len(upper_line_2) > 0:
                                rel_dots.append(second_blob)
                            if len(upper_line_3) > 0:
                                rel_dots.append(third_blob)

                            print(len(rel_dots))
                            if len(rel_dots) == 2:
                                message = 3

                            if len(rel_dots) == 1:
                                blob = rel_dots[0]
                                roi_left = [0, blob.y(), blob.x(), blob.y() + blob.h()]
                                roi_right = [blob.x(), blob.y(), width - blob.x(), blob.y() + blob.h()]
                                roi_top = [blob.x(), 0, blob.x() + blob.w(), blob.y()]
                                upper_line = img.find_blobs(threshold_line, False, roi_top, area_threshold=900)
                                left_line = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
                                right_line = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)

                                if len(upper_line) != 0:
                                    if len(left_line) != 0:
                                        message = 2
                                    elif len(right_line) != 0:
                                        message = 1
                                """
                elif len(blobs) == 4:
                    message = 3

                else:
                    message = 0
            communication(message)
    main()
"""
uart table:
0 = foreward
1 = left
2 = right
3 = trun around
5 = blob detected
"""
