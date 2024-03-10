import matplotlib.pyplot as plt
import numpy as np

from PIL import Image


def upscale_img(path: str, return_path, scale=10):
    img = plt.imread(path)
    new_img = np.zeros((img.shape[0] * scale, img.shape[1] * scale, img.shape[2]), dtype=float)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x, y, :]
            
            new_img[x * scale:(x + 1) * scale, y * scale:(y + 1) * scale, :] = pixel
            
    plt.imsave(return_path, new_img)
    