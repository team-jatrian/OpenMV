#created by Sin(an)

import sensor, image
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

while(True):
    def distance():
        img = sensor.snapshot()
        circles = img.find_circles(threshold=300)
        if len(circles) == 1:
            for c in circles:
                img.draw_circle(c.x(), c.y(), c.r())
                img.draw_line(80, 60, c.x(), c.y(), 200)
                distance = -(80 - c.x())
        else:
            print("Oh oh, no circles around! or too many circles")
            distance = 0
        return distance
    print(distance())

