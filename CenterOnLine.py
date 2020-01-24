#created by Sin(an)
import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)

threshold_line = [(0, 33, -128, 127, -128, 127)]

roi_top = [0, 0, 80, 20]
roi_middle = [0, 20, 80, 20]
roi_bottom= [0, 40, 80, 20]

accuracy = 3
rois = [None] * accuracy
xVals = [None] * accuracy

while(1):
   img = sensor.snapshot()
   def splitter():
       for roi in enumerate(rois):
            loop_index = roi[0]
            width = 80
            general_height = int(60/len(rois))
            single = loop_index * general_height
            xVals[loop_index] = single
            rois[loop_index] = [0, xVals[loop_index], 80, general_height]
            blobs = img.find_blobs(threshold_line, False, rois[loop_index])
            img.draw_rectangle(rois[loop_index])
            print(len(blobs))
        for blob in blobs:
            img.draw_rectangle(blob.x(), blob.y(), blob.w(), blob.y())

   splitter()
