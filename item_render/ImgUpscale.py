import os

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, UnidentifiedImageError


def upscale_img(path: str, return_path, scale=10):
    img = plt.imread(path)
    new_img = np.zeros((img.shape[0] * scale, img.shape[1] * scale, img.shape[2]), dtype=float)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x, y, :]

            new_img[x * scale:(x + 1) * scale, y * scale:(y + 1) * scale, :] = pixel

    plt.imsave(return_path, new_img)


def upscale_entire_folder(path: str, scale, return_path):
    for img_path in os.listdir(path):
        try:
            upscale_img(path + '/' + img_path, return_path + '/' + img_path, scale=scale)
        except UnidentifiedImageError:
            pass
        except IsADirectoryError:
            pass


folder_id = '/Users/andrewyin/Desktop/code'
minecraft = 'minecraft-assets-1.20.4/assets/minecraft/textures/item'


def get_path_for_id(mod_id: str = None, block=False):
    return f'/Users/andrewyin/Desktop/code/{mod_id.replace('_', '-')}/src/main/resources/assets/{mod_id}/textures/{'block' if block else 'item'}'


def get_return_path_from_id(scale, mod_id: str = None):
    return f'/Users/andrewyin/Desktop/wiki/{mod_id}_img/{'32x' if scale == 2 else '160x'}'


def move_for_render(modid, block_name):
    img = plt.imread(get_path_for_id(modid, True) + '/' + block_name + '.png')
    plt.imsave(
        '/Users/andrewyin/Desktop/Minecraft/fabric_stuff/resourcepacks/test_test_test/assets/minecraft/textures/block/acacia_planks.png',
        img)


CC = 'caverns_and_chasms'
neapolitan = 'neapolitan'
BG = 'berry_good'
INC = 'incubation'



