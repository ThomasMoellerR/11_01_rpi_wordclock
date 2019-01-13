import numpy as np
import colorsys
import random

def grad_to_rgb(grad):
    color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
    color = np.asarray(color)
    color *= 255
    r = color[0]
    g = color[1]
    b = color[2]
    return r,g,b


class wordclock:

    wordidx = {}
    wordidx["es"] = (0,1)
    wordidx["ist"] = (3,4,5)
    wordidx["funf"] = (7,8,9,10)
    wordidx["zehn"] = (11,12,13,14)
    wordidx["zwanzig"] = (15,16,17,18,19,20,21)
    wordidx["drei"] = (22,23,24,25)
    wordidx["viertel"] = (26,27,28,29,30,31,32)
    wordidx["nach"] = (35,36,37,38)
    wordidx["vor"] = (39,40,41)
    wordidx["halb"] = (44,45,46,47)
    wordidx["zwolf"] = (49,50,51,52,53)
    wordidx["zw"] = (55,56)
    wordidx["ei"] = (57,58)
    wordidx["n"] = (59,)
    wordidx["s"] = (60,)
    wordidx["ieben"] = (61,62,63,64,65)
    wordidx["drei_2"] = (67,68,69,70)
    wordidx["funf_2"] = (73,74,75,76)
    wordidx["elf"] = (77,78,79)
    wordidx["neun"] = (80,81,82,83)
    wordidx["vier"] = (84,85,86,87)
    wordidx["acht"] = (89,90,91,92)
    wordidx["zehn_2"] = (93,94,95,96)
    wordidx["sechs"] = (100,101,102,103,104)
    wordidx["uhr"] = (107,108,109)
    wordidx["1min"] = (113,)
    wordidx["2min"] = (110,)
    wordidx["3min"] = (111,)
    wordidx["4min"] = (112,)



    def __init__(self):
        self.mode = "WORD_RANDOM_COLOR"
        self.brightness = 1.0
        self.uniquewords_pixelmap = np.zeros((114), dtype=np.uint8)
        self.rgb_pixelmap = np.zeros((114,3), dtype=np.uint8)
        self.rgb_brightness_pixelmap = np.zeros((114,3), dtype=np.uint8)
        self.fixed_color = (0,255,0)

    def random_pixels(self):
        self.rgb_brightness_pixelmap = np.zeros((114,3), dtype=np.uint8)

        color = (255,255,255)
        self.rgb_brightness_pixelmap[110] = color
        self.rgb_brightness_pixelmap[111] = color
        self.rgb_brightness_pixelmap[112] = color
        self.rgb_brightness_pixelmap[113] = color


    def get_pixelmap(self):
        return self.rgb_brightness_pixelmap.tolist()

    def set_color (self, color):
        self.fixed_color = color

    def set_mode(self, mode):
        self.mode = mode


    def set_brightness(self, brightness):
        self.brightness = brightness
        self.fill_rgb_brightness_pixelmap()

    def set_time(self, hours, minutes):
        if self.mode == "SAME_COLOR" or self.mode == "WORD_RANDOM_COLOR" or self.mode == "CHARACTER_RANDOM_COLOR":
            self.calcualte_uniquewords_pixelmap(hours, minutes)


    def update(self):
        self.fill_rgb_pixelmap()
        self.fill_rgb_brightness_pixelmap()


    def fill_rgb_pixelmap(self):
        if self.mode == "SAME_COLOR" or self.mode == "WORD_RANDOM_COLOR" or self.mode == "CHARACTER_RANDOM_COLOR":

            self.rgb_pixelmap = np.zeros((114,3), dtype=np.uint8)

            for i in np.trim_zeros(np.unique(self.uniquewords_pixelmap)):
                for j in np.where(self.uniquewords_pixelmap == i):

                    if self.mode == "SAME_COLOR":
                        for k in j:
                            self.rgb_pixelmap[k] = self.fixed_color

                    if self.mode == "WORD_RANDOM_COLOR":
                        grad = random.choice(np.arange(0,360,1))
                        r,g,b = grad_to_rgb(grad)
                        for k in j:
                            self.rgb_pixelmap[k] = (r,g,b)

                    if self.mode == "CHARACTER_RANDOM_COLOR":
                        for k in j:
                            grad = random.choice(np.arange(0,360,1))
                            r,g,b = grad_to_rgb(grad)
                            self.rgb_pixelmap[k] = (r,g,b)

        if self.mode == "TEST":
            for i in range(len(self.rgb_pixelmap)):
                self.uniquewords_pixelmap[i] = 1 # ungleich null
                self.rgb_pixelmap[i] = self.fixed_color




    def fill_rgb_brightness_pixelmap(self):
        self.rgb_brightness_pixelmap = np.zeros((114,3), dtype=np.uint8)

        for i in range(len(self.uniquewords_pixelmap)):
            if self.uniquewords_pixelmap[i] != 0:
                h,s,v = colorsys.rgb_to_hsv(self.rgb_pixelmap[i][0] / 255, self.rgb_pixelmap[i][1] / 255, self.rgb_pixelmap[i][2] / 255)
                v = self.brightness
                r,g,b = colorsys.hsv_to_rgb(h,s,v)
                self.rgb_brightness_pixelmap[i][0] = r * 255
                self.rgb_brightness_pixelmap[i][1] = g * 255
                self.rgb_brightness_pixelmap[i][2] = b * 255

    def set_pixel(self, words, increase_counter):
        if increase_counter: self.uncounter += 1
        for i in words: self.uniquewords_pixelmap[i] = self.uncounter

    def calcualte_uniquewords_pixelmap(self, hours, minutes):
        self.uniquewords_pixelmap = np.zeros((114), dtype=np.uint8)
        self.uncounter = 0

        # Immer
        self.set_pixel(wordclock.wordidx["es"], 1)
        self.set_pixel(wordclock.wordidx["ist"], 1)
        self.set_pixel(wordclock.wordidx["uhr"], 1)

        # Stunden
        if hours == 0 or hours == 12 or hours == 24:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["zwolf"], 1)
            else:
                self.set_pixel(wordclock.wordidx["ei"], 1)
                self.set_pixel(wordclock.wordidx["n"], 0)
                self.set_pixel(wordclock.wordidx["s"], 0)

        if hours == 1 or hours == 13:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["ei"], 1)
                self.set_pixel(wordclock.wordidx["n"], 0)
                self.set_pixel(wordclock.wordidx["s"], 0)
            else:
                self.set_pixel(wordclock.wordidx["zw"], 1)
                self.set_pixel(wordclock.wordidx["ei"], 0)

        if hours == 2 or hours == 14:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["zw"], 1)
                self.set_pixel(wordclock.wordidx["ei"], 0)
            else:
                self.set_pixel(wordclock.wordidx["drei_2"], 1)

        if hours == 3 or hours == 15:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["drei_2"], 1)
            else:
                self.set_pixel(wordclock.wordidx["vier"], 1)

        if hours == 4 or hours == 16:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["vier"], 1)
            else:
                self.set_pixel(wordclock.wordidx["funf_2"], 1)

        if hours == 5 or hours == 17:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["funf_2"], 1)
            else:
                self.set_pixel(wordclock.wordidx["sechs"], 1)

        if hours == 6 or hours == 18:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["sechs"], 1)
            else:
                self.set_pixel(wordclock.wordidx["s"], 1)
                self.set_pixel(wordclock.wordidx["ieben"], 0)

        if hours == 7 or hours == 19:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["s"], 1)
                self.set_pixel(wordclock.wordidx["ieben"], 0)
            else:
                self.set_pixel(wordclock.wordidx["acht"], 1)

        if hours == 8 or hours == 20:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["acht"], 1)
            else:
                self.set_pixel(wordclock.wordidx["neun"], 1)

        if hours == 9 or hours == 21:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["neun"], 1)
            else:
                self.set_pixel(wordclock.wordidx["zehn_2"], 1)

        if hours == 10 or hours == 22:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["zehn_2"], 1)
            else:
                self.set_pixel(wordclock.wordidx["elf"], 1)

        if hours == 11 or hours == 23:
            if minutes < 25:
                self.set_pixel(wordclock.wordidx["elf"], 1)
            else:
                self.set_pixel(wordclock.wordidx["zwolf"], 1)

        # 5 Mintuen Schritte
        if minutes >= 0 and minutes <= 4:
            pass

        if minutes >= 5 and minutes <= 9:
            self.set_pixel(wordclock.wordidx["funf"], 1)
            self.set_pixel(wordclock.wordidx["nach"], 1)

        if minutes >= 10 and minutes <= 14:
            self.set_pixel(wordclock.wordidx["zehn"], 1)
            self.set_pixel(wordclock.wordidx["nach"], 1)

        if minutes >= 15 and minutes <= 19:
            self.set_pixel(wordclock.wordidx["viertel"], 1)
            self.set_pixel(wordclock.wordidx["nach"], 1)

        if minutes >= 20 and minutes <= 24:
            self.set_pixel(wordclock.wordidx["zwanzig"], 1)
            self.set_pixel(wordclock.wordidx["nach"], 1)

        if minutes >= 25 and minutes <= 29:
            self.set_pixel(wordclock.wordidx["funf"], 1)
            self.set_pixel(wordclock.wordidx["vor"], 1)
            self.set_pixel(wordclock.wordidx["halb"], 1)

        if minutes >= 30 and minutes <= 34:
            self.set_pixel(wordclock.wordidx["halb"], 1)

        if minutes >= 35 and minutes <= 39:
            self.set_pixel(wordclock.wordidx["funf"], 1)
            self.set_pixel(wordclock.wordidx["nach"], 1)
            self.set_pixel(wordclock.wordidx["halb"], 1)

        if minutes >= 40 and minutes <= 44:
            self.set_pixel(wordclock.wordidx["zwanzig"], 1)
            self.set_pixel(wordclock.wordidx["vor"], 1)

        if minutes >= 45 and minutes <= 49:
            self.set_pixel(wordclock.wordidx["viertel"], 1)
            self.set_pixel(wordclock.wordidx["vor"], 1)

        if minutes >= 50 and minutes <= 54:
            self.set_pixel(wordclock.wordidx["zehn"], 1)
            self.set_pixel(wordclock.wordidx["vor"], 1)

        if minutes >= 55 and minutes <= 59:
            self.set_pixel(wordclock.wordidx["funf"], 1)
            self.set_pixel(wordclock.wordidx["vor"], 1)

        # Minuten
        for j in range(1,60,5):
            if minutes == j:
                self.set_pixel(wordclock.wordidx["1min"], 1)
                break

        for j in range(2,60,5):
            if minutes == j:
                self.set_pixel(wordclock.wordidx["1min"], 1)
                self.set_pixel(wordclock.wordidx["2min"], 1)
                break

        for j in range(3,60,5):
            if minutes == j:
                self.set_pixel(wordclock.wordidx["1min"], 1)
                self.set_pixel(wordclock.wordidx["2min"], 1)
                self.set_pixel(wordclock.wordidx["3min"], 1)
                break

        for j in range(4,60,5):
            if minutes == j:
                self.set_pixel(wordclock.wordidx["1min"], 1)
                self.set_pixel(wordclock.wordidx["2min"], 1)
                self.set_pixel(wordclock.wordidx["3min"], 1)
                self.set_pixel(wordclock.wordidx["4min"], 1)
                break
