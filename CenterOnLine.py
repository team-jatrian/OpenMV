#created by Sin(an)
import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)

threshold_line = [(0, 33, -128, 127, -128, 127)]

width = sensor.width()
height = sensor.height()

accuracy = 4
rois = [None] * accuracy
xValues = [None] * accuracy
all_blobs_N = [None] * accuracy
yVals = []
xVals = []
while(1):
   img = sensor.snapshot()
   def line_finder():
       for roi in enumerate(rois):
            global all_blobs

            loop_index = roi[0]
            general_height = int(height/len(rois))
            single = loop_index * general_height
            xValues[loop_index] = single
            rois[loop_index] = [0, xValues[loop_index], width, general_height]
            blobs = img.find_blobs(threshold_line, False, rois[loop_index])
            all_blobs_N[loop_index] = blobs

            img.draw_rectangle(rois[loop_index])
            for blob in blobs:
                img.draw_rectangle(blob.rect())

            all_blobs = []
            for val in all_blobs_N:
                 if val != []:
                     all_blobs.append(val)

            for i in range(len(all_blobs)):
                global yVals
                global xVals

                if len(yVals) < len(all_blobs):
                    yVals.append(all_blobs[i][0].y())
                    xVals.append(all_blobs[i][0].x())
            index_of_low_y = yVals.index(min(yVals))
            index_of_high_y = yVals.index(max(yVals))

            print(xVals[index_of_high_y])
            print(xVals[index_of_low_y])
            lowest_y = min(yVals)
            highest_y = max(yVals)
            print(lowest_y)
            print(highest_y)
            return lowest_y, highest_y
   line_finder()
