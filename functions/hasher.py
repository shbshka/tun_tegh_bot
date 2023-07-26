import os
from PIL import Image, ImageChops

def is_different_image(image):
    a = True
    image = Image.open(image)
    for file in os.listdir("./screenshots"):
        file = Image.open("./screenshots/" + file)
        result = ImageChops.difference(image, file).getbbox()
        if result == None:
            a = False
    return a
