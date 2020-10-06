from PIL import Image


def save_resized_image(im, dir):
    nw, nh = im.size


#Resize an image to a given with and height.
def resize_image(fp: str, width, height):
    im = Image.open(fp)
    new_dim: tuple = (width, height)
    return im.resize(new_dim)


""" Resize an image maintaining its proportions
    Args:
        fp (str): Path argument to image file
        scale (Union[float, int]): Percent as whole number of original image. eg. 53
    Returns:
        image (np.ndarray): Scaled image
    """
"""
def resize_image_proportional(fp: str, scale: Union[float, int]) -> np.ndarray:
    _scale = lambda dim, s: int(dim * s / 100)
    im = Image.open(fp)
    width, height = im.size
    new_width: int = _scale(width, scale)
    new_height: int = _scale(height, scale)
    new_dim: tuple = (new_width, new_height)
    return im.resize(new_dim)
"""