# Source code for screen capturing and clicking from:
# http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

import time
from PIL import ImageGrab, Image
import convnetpy.deepqlearn
# import matplotlib.pyplot as plt
from game_utils import FlappyGeneratorGame, FlappyBirdIO
from IOUtilsWin import IOUtilsWin

INPUT_SIZE = (60, 60)
TEMPORAL_WINDOW = 1
NUM_ACTIONS = 2

game = FlappyGeneratorGame()
# game = FlappyBirdIO()
io_utils = IOUtilsWin(game.screen_info['X_PAD'], game.screen_info['Y_PAD'])


def screenGrab(screen_info):
    box = (screen_info['X_PAD'],
           screen_info['Y_PAD'],
           screen_info['X_PAD'] + screen_info['GAME_WIDTH'],
           screen_info['Y_PAD'] + screen_info['GAME_HEIGHT'])
    image = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return image


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

    tdtrainer_options = {'learning_rate': 0.01, 'momentum': 0.0, 'batch_size': 3, 'l2_decay': 0.0}

    opt = {}
    opt['temporal_window'] = TEMPORAL_WINDOW
    opt['experience_size'] = 30000
    opt['start_learn_threshold'] = 10
    opt['gamma'] = 0.9
    opt['learning_steps_total'] = 100
    opt['learning_steps_burnin'] = 10
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
        image = screenGrab(game.screen_info)
        is_end = game.isEnd(image)
        # print(is_end)
        if is_end:
            # brain.backward(-1000)
            brain.giveReward(-20)
            print("Training...")
            brain.train()
            # brain.clearExperience()
            io_utils.restart()
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
            io_utils.fly()
        time.sleep(0.3)


if __name__ == '__main__':
    main()
