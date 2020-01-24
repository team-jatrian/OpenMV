#created by Sin(an)

import sensor, image

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

threshold_blobs = [(29, 0, -34, -3, -26, 9)]
threshold_line = [(1, 1, 1, 1, 1 ,1)]

roi_blobs = [0, 180, 320, 60]

while(True):
    img = sensor.snapshot()
    blobs = img.find_blobs(threshold_blobs, False, roi_blobs)

    if len(blobs) == 1:
        if blob
    elif len(blobs) == 2:
    elif len(blobs) == 3:
    elif len(blobs) == 4:
