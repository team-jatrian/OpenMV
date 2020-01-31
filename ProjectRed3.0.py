import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)
threshold_blobs = [(48, 20, -128, -22, -128, 127)]
threshold_line = [(39, 0, -11, 127, -128, 127)]
roi_blobs = [0, 130, 320, 110]
height = sensor.height()
width = sensor.width()
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
        blobs = img.find_blobs(threshold_blobs, False, roi_blobs, merge=True, x_stride=10, y_stride=10, area_threshold=900)
        if len(blobs) > 0:
            communication(5)
        for blob in blobs:
            img.draw_rectangle(blob.rect())
            if len(blobs) == 1:
                roi_left = [0, blob.y(), blob.x(), blob.y() + blob.h()]
                roi_right = [blob.x(), blob.y(), width - blob.x(), blob.y() + blob.h()]
                roi_top = [blob.x(), 0, blob.x() + blob.w(), blob.y()]
                roi_bottom = [blob.x(), blob.y(), blob.w(), height-blob.y()]
                img.draw_rectangle(roi_left, 900)
                img.draw_rectangle(roi_right, 300)
                img.draw_rectangle(roi_top, 50)
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
                roi_left_1 = [0, first_blob.y(), first_blob.x(), first_blob.y() + first_blob.h()]
                roi_right_1 = [first_blob.x(), first_blob.y(), width, first_blob.y() + first_blob.h()]
                roi_top_1 = [first_blob.x(), 0, first_blob.x() + first_blob.w(), first_blob.y()]
                second_blob = blobs[1]
                roi_left_2 = [0, second_blob.y(), second_blob.x(), second_blob.y() + second_blob.h()]
                roi_right_2 = [second_blob.x(), second_blob.y(), width, second_blob.y() + second_blob.h()]
                roi_top_2 = [second_blob.x(), 0, second_blob.x() + second_blob.w(), second_blob.y()]
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
                first_blob = blobs[0]
                second_blob = blobs[1]
                third_blob = blobs[2]
                all_blobs = [first_blob, second_blob, third_blob]
                yVals = [first_blob.y(), second_blob.y(), third_blob.y()]
                highestY = yVals.index(min(yVals))
                rel_blob = all_blobs[highestY]
                roi_left = [0, rel_blob.y(), rel_blob.x(), rel_blob.y() + rel_blob.h()]
                roi_right = [rel_blob.x(), rel_blob.y(), width, rel_blob.y() + rel_blob.h()]
                roi_top = [rel_blob.x(), 0, rel_blob.x() + rel_blob.w(), rel_blob.y()]
                try:
                    upper_line = img.find_blobs(threshold_line, False, roi_top, area_threshold=900)
                    left_line = img.find_blobs(threshold_line, False, roi_left, area_threshold=900)
                    right_line = img.find_blobs(threshold_line, False, roi_right, area_threshold=900)
                except:
                    break
                if len(upper_line) != 0:
                    if len(left_line) != 0:
                        message = 2
                    elif len(right_line) != 0:
                        message = 1
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
