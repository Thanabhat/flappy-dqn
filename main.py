# Source code for screen capturing and clicking from:
# http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

import sys

sys.path.insert(0, 'C:\Program Files (x86)\Python35-32\lib\site-packages')

# import os
import time
from PIL import ImageGrab, Image
import win32api, win32con
import numpy as np
import convnetpy.deepqlearn
# import matplotlib.pyplot as plt

## http://flappy-generator.com/?id=572e177e5d02a
X_PAD = 247
Y_PAD = 178
GAME_WIDTH = 467
GAME_HEIGHT = 622

## http://flappybird.io/
# X_PAD = 105
# Y_PAD = 203
# GAME_WIDTH = 480
# GAME_HEIGHT = 640

INPUT_SIZE = (60, 60)
TEMPORAL_WINDOW = 1
NUM_ACTIONS = 2


def screenGrab():
    box = (X_PAD, Y_PAD, X_PAD + GAME_WIDTH, Y_PAD + GAME_HEIGHT)
    image = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return image


def isEndFlappyBirdGenerator(image):
    ## http://flappy-generator.com/

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


def isEndFlappyBirdIO(image):
    ## http://flappybird.io/
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


def restart():
    time.sleep(0.5)
    mousePos((110, 370))
    leftClick()
    time.sleep(0.5)
    fly()


def fly():
    mousePos((10, 10))
    leftClick()


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((X_PAD + cord[0], Y_PAD + cord[1]))


def buildDeepQNetwork():
    num_inputs = INPUT_SIZE[0] * INPUT_SIZE[1]

    layer_defs = []

    layer_defs.append(
        {'type': 'input', 'out_sx': INPUT_SIZE[0], 'out_sy': INPUT_SIZE[1], 'out_depth': TEMPORAL_WINDOW + 1})
    layer_defs.append({'type': 'conv', 'sx': 6, 'filters': 8, 'stride': 3, 'pad': 0, 'activation': 'relu'})
    layer_defs.append({'type': 'conv', 'sx': 4, 'filters': 8, 'stride': 2, 'pad': 0, 'activation': 'relu'})
    layer_defs.append({'type': 'fc', 'num_neurons': 64, 'activation': 'relu'})
    layer_defs.append({'type': 'regression', 'num_neurons': NUM_ACTIONS})

    # layer_defs.append({'type': 'input', 'out_sx': INPUT_SIZE[0], 'out_sy': INPUT_SIZE[1], 'out_depth': 1})
    # layer_defs.append({'type': 'conv', 'sx': 8, 'filters': 32, 'stride': 4, 'pad': 0})
    # layer_defs.append({'type': 'pool', 'sx': 2, 'stride': 2})
    # layer_defs.append({'type': 'conv', 'sx': 4, 'filters': 32, 'stride': 2, 'pad': 0})
    # layer_defs.append({'type': 'pool', 'sx': 2, 'stride': 2})
    # layer_defs.append({'type': 'conv', 'sx': 3, 'filters': 64, 'stride': 1, 'pad': 0})
    # layer_defs.append({'type': 'pool', 'sx': 2, 'stride': 2})
    # layer_defs.append({'type': 'fc', 'num_neurons': 256, 'activation': 'relu'})
    # layer_defs.append({'type': 'regression', 'num_neurons': NUM_ACTIONS})

    tdtrainer_options = {'learning_rate': 0.01, 'momentum': 0.0, 'batch_size': 64, 'l2_decay': 0.0}

    opt = {}
    opt['temporal_window'] = TEMPORAL_WINDOW
    opt['experience_size'] = 30000
    opt['start_learn_threshold'] = 1000
    opt['gamma'] = 0.9
    opt['learning_steps_total'] = 10000
    opt['learning_steps_burnin'] = 1000
    opt['epsilon_min'] = 0.01
    opt['epsilon_max'] = 1.0
    # opt['learning_steps_total'] = 200000
    # opt['learning_steps_burnin'] = 3000
    # opt['epsilon_min'] = 0.05
    opt['epsilon_test_time'] = 0.05
    opt['layers'] = layer_defs
    opt['tdtrainer_options'] = tdtrainer_options

    brain = convnetpy.deepqlearn.Brain(num_inputs, NUM_ACTIONS, opt)

    return brain


def prepareImageInput(image):
    image = image.resize((INPUT_SIZE[0], INPUT_SIZE[1]), Image.ANTIALIAS)
    image = image.convert("L")

    # arr = np.asarray(image)
    # plt.imshow(arr, cmap='Greys_r')
    # plt.show()

    # image.save(os.getcwd() + '\\data_log\\' + str((time.time())) + '_input.png', 'PNG')

    input_list = []
    for y in range(INPUT_SIZE[1]):
        for x in range(INPUT_SIZE[0]):
            input_list.append(image.getpixel((x, y)) / 256.0)
    return input_list


def main():
    N_GAME = 1000000
    cnt = 0
    brain = buildDeepQNetwork()
    while True:
        image = screenGrab()
        is_end = isEndFlappyBirdGenerator(image)
        # print(is_end)
        if is_end:
            # brain.backward(-1000)
            brain.giveReward(-20)
            print("Training...")
            brain.train()
            # brain.clearExperience()
            restart()
            cnt += 1
            print("#### Game %d ####" % cnt)
            if cnt == N_GAME:
                break
        else:
            brain.giveReward(1)
        input_list = prepareImageInput(image)
        action = brain.forward(input_list)
        # print('action=%d' % action)
        if action == 0:
            fly()
        time.sleep(0.3)


if __name__ == '__main__':
    main()
