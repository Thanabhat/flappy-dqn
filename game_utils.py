import numpy as np


# http://flappy-generator.com/?id=572e177e5d02a
class FlappyGeneratorGame:
    def __init__(self):
        self.screen_info = {
            'X_PAD': 247,
            'Y_PAD': 178,
            'GAME_WIDTH': 467,
            'GAME_HEIGHT': 622
        }

    def isEnd(self, image):
        # check not white
        cnt_white = 0
        cnt_all = 0
        for x in range(206, 258):
            for y in range(33, 80):
                color = image.getpixel((x, y))
                if color[0] >= 245 and color[1] >= 245 and color[2] >= 245:
                    cnt_white += 1
                cnt_all += 1
        if 1.0 * cnt_white / cnt_all < 0.3:
            return True

        # check score appear
        color = np.zeros((3))
        cnt = 0
        for x in range(225, 230):
            for y in range(198, 203):
                color = np.add(color, image.getpixel((x, y)))
                cnt += 1
        color /= cnt
        if color[0] >= 245 and color[1] >= 245 and color[2] >= 245:
            return True
        return False


## http://flappybird.io/
class FlappyBirdIO:
    def __init__(self):
        self.screen_info = {
            'X_PAD': 105,
            'Y_PAD': 203,
            'GAME_WIDTH': 480,
            'GAME_HEIGHT': 640
        }

    def isEnd(self, image):
        color = np.zeros((3))
        cnt = 0
        for x in range(106, 110):
            for y in range(367, 371):
                color = np.add(color, image.getpixel((x, y)))
                cnt += 1
        color /= cnt
        if color[0] >= 220 and color[0] < 250 \
                and color[1] >= 90 and color[1] < 110 \
                and color[2] >= 0 and color[2] < 15:
            return True
        return False
