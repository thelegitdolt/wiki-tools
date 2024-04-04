from PIL import Image


def crop_426(name=None):
    img = Image.open('/Users/andrewyin/Desktop/Minecraft/fabric_stuff/renders/acacia_planks.png')

    a = img.crop((58, 43, 358, 343))
    a.save('/Users/andrewyin/Desktop/sex.png')


def crop_46(name=None):
    img = Image.open('/Users/andrewyin/Desktop/Minecraft/fabric_stuff/renders/acacia_planks.png')

    a = img.crop((7, 5, 39, 37))
    a.save('/Users/andrewyin/Desktop/sex.png')
