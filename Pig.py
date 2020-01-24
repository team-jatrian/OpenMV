#created by Sin(an)
import sensor, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)

uart = pyb.UART(3, 115200, timeout_char=1000, bits=8, parity=1, stop=2)

threshold_line = [(0, 37, -13, 127, 127, -128)]
threshold_dots = [(0, 37, -13, -128, -13, 127)]

equator = 0
meridian = 0
dots = 0
dot = 0
direction = 0
roi_middle = [0, 25, 80, 35]
red_led = pyb.LED(1)
green_led = pyb.LED(2)
blue_led = pyb.LED(3)
while(True):
    img = sensor.snapshot()

    red_led.on()
    green_led.on()
    blue_led.on()
    img = sensor.snapshot()
    def line_detection():
        global equator
        global meridian
        #Lineare Regression nutzen, um Linie zu erkennen
        line_v = img.get_regression(threshold_line, robust=True)
        #Den Durchschnit der vertikalen Linie festlegen
        try:
            meridian = int((line_v.x1() + line_v.x2()) / 2)
        except:
            meridian = 0

        img.draw_line(meridian, 0, meridian, 60, 900)

        #Seitenränder als ROI einstellen
        roi_1 = [0, 0, 15, 60]
        roi_2 = [65, 0, 15, 60]

        line_h_1 = img.find_blobs(threshold_line, False, roi_1, merge=True)
        line_h_2 = img.find_blobs(threshold_line, False, roi_2, merge=True)

        #Standard Y-Koordinaten bestimmen
        y_first = 0
        y_second = 0
        #Y-Koordinaten für Spezialfälle bestimmen
        if len(line_h_2) != 0 and len(line_h_1) != 0:
            for blob in line_h_2:
                y_second = blob.cy()
            for blob in line_h_1:
                y_first = blob.cy()
        elif len(line_h_2) == 0:
            for blob in line_h_1:
                y_first = blob.cy()
                y_second = y_first
        elif len(line_h_1) == 0:
            for blob in line_h_2:
                y_second = blob.cy()
                y_first = y_second
        elif len(line_h_2) == 0 and len(line_h_1) == 0:
            y_first = 0
            y_second = 0

        img.draw_line(0, y_first, 80, y_second, 400)
        #Den Durchschnitt der horizontalen Linie festlegen
        equator = int((y_first + y_second) / 2)

        if equator != 0:
            return meridian, equator
        else:
            return 0, 0

    def color_detection():
        global dots
        global dot
        global direction

        dots = img.find_blobs(threshold_dots)
        if dots:
            for dot in dots:
                img.draw_rectangle(dot.rect())
            compare_dots(len(dots), line_detection()[0], line_detection()[1])
        else:
            print("Oh oh no blobs around!")
            direction = 0
        uart.write("%d"%direction)
        print(direction)
        middle_checker()

    def compare_dots(amount, meridian, equator):

       global dots
       global dot
       global direction

       #check the amount of dots and compare them
       if amount == 1:
            one = dots[0]
            if one.y() > equator:
                if one.x() > meridian:
                    direction = 2
                elif one.x() < meridian:
                    direction = 1
            else:
                direction = 0

       elif amount == 2:
            one = dots[0]
            two = dots[1]
            if one.y() or two.y() > equator:

                #check wich dot is relevant / has the higher y-value
                if one.y() < two.y():
                    rel_dot = two
                else:
                    rel_dot = one

                if rel_dot.x() < meridian:
                    direction = 1
                elif rel_dot.x() > meridian:
                    direction = 2
            elif one.y() and two.y() > equator:
                    direction = 3
            elif one.y() and two.y() < equator:
                direction = 0

       elif amount == 3:
            one = dots[0]
            two = dots[1]
            three = dots[2]
            if one.y() and two.y() > equator:
                direction = 3
            elif three.y() and one.y() > equator:
                direction = 3
            elif three.y() and two.y() > equator:
                direction = 3
            else:
                #check wich dot is relevant / has the higher y-value
                if one.y() > two.y():
                    rel_dot = one
                if one.y() < two.y():
                    rel_dot = two
                if two.y() > three.y():
                    rel_dot = two
                if two.y() < three.y():
                    rel_dot = three
                if one.y() > three.y():
                    rel_dot = one
                if one.y() < three.y():
                    rel_dot = three
                else:
                    color_detection()

                if rel_dot.x() < meridian:
                    direction = 1
                elif rel_dot.x() > meridian:
                    direction = 2
       elif amount == 4:
            direction = 3

    def middle_detection():
        all_dots = img.find_blobs(threshold_dots)
        middle_dots = img.find_blobs(threshold_dots, False, roi_middle)
        all_amount = len(all_dots)
        middle_amount = len(middle_dots)
        for blob in all_dots:

            for blob_middle in middle_dots:
                if middle_amount == all_amount:
                    return 5
                else:
                    return 0
                return 0
    def middle_checker():
        img.draw_rectangle(roi_middle)
        dotsInMiddle = middle_detection()
        if dotsInMiddle == 5:
            uart.write("%d"%dotsInMiddle)
            print(dotsInMiddle)
            color_detection()
    middle_checker()

"""
Direction Tabel:
0 = Gerade
1 = Links
2 = Rechts
3 = 180° Drehen
69 = Blobs are in range
"""
