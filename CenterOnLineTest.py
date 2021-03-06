#created by Sin(an)
import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
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


def line_finder():
    img = sensor.snapshot()
    for roi in enumerate(rois):
        global all_blobs
        loop_index = roi[0]
        general_height = int(height/len(rois))
        single = loop_index * general_height
        xValues[loop_index] = single
        rois[loop_index] = [0, xValues[loop_index], width, general_height]
        blobs = img.find_blobs(threshold_line, False, rois[loop_index])
        all_blobs_N[loop_index] = blobs

        all_blobs = []
        for val in all_blobs_N:
             if val != []:
                 all_blobs.append(val)
    return all_blobs
def sachen():
    img = sensor.snapshot()
    global yVals
    global xVals
    xVals.clear()
    for i in range(len(line_finder())):
        xVals.append(line_finder()[i][0].x())
        yVals.append(line_finder()[i][0].y())

    index_of_low_y = yVals.index(min(yVals))
    index_of_high_y = yVals.index(max(yVals))

    difference = xVals[index_of_high_y] - xVals[index_of_low_y]
    print(difference)
    uart.write("%d"%difference + "\n")
while(1):
    sachen()

