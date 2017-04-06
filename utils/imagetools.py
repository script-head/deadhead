from PIL import Image

def rescale(image, dimensions):
    image.thumbnail(dimensions, Image.ANTIALIAS)
    return image