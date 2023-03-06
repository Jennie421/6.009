#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y):
    """
    Return the color of pixel at position (x, y) of a given image. 
    """
    index = x * image['width'] + y
    return image['pixels'][index]

def handel_out_of_bound(image, x, y):
    """
    Return the color of a pixel at position (x, y) of a given image. 
    Out-of-bound pixels are considered to have identical color with the nearet edge pixels of the image.
    """
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x >= image['height']:
        x = image['height'] - 1
    if y >= image['width']: 
        y = image['width'] - 1

    index = x * image['width'] + y

    return image['pixels'][index]


def set_pixel(image, c):
    """
    Append a new pixel with color `c` to a given image.
    """
    image['pixels'].append(c)


def apply_per_pixel(image, func):
    """
    Apply a function to modify each pixel in a given image. 
    Return a new modifed image. 
    """
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    for x in range(image['height']):
        for y in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, newcolor)
    return result


def inverted(image):
    """
    Return a new image representing the result of inverting a given image.
    """
    return apply_per_pixel(image, lambda c: 255-c)


def kernel(image, kernel):
    """
    Return a new image representing the result of correlating a given kernel with a given image.
    """
    result = correlate(image, kernel)
    result = round_and_clip_image(result)
    return result 

# below are different kernels used to modify images 
identity_kernel = [[0,0,0],[0,1,0],[0,0,0]]

translation_kernel=[[0,0,0,0,0],
                    [0,0,0,0,0],
                    [1,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
    
average_kernel=[[0.0,0.2,0.0],
                [0.2,0.2,0.2],
                [0.0,0.2,0.0]]

nine_by_nine_kernel=[[0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0]]

# HELPER FUNCTIONS

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    A kernel is represented as an n x n matrix. 
    """
    def kernel_calc(pixel, x, y, kernel):
        """
        Compute and return the new color of a pixel of an image given its position and a kernel.
        """
        new = 0; 
        kernel_size = len(kernel)
        # Relative positions to current pixel
        offset = range(-((kernel_size - 1) // 2), 1 + kernel_size // 2)
        
        # Absolute positions in the kernel
        kernel_index = range(kernel_size)
        
        for dx, kx in zip(offset, kernel_index):
            for dy, ky in zip(offset, kernel_index):
                new += handel_out_of_bound(image, x+dx, y+dy) * kernel[kx][ky]
        return new
 
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    
    for x in range(image['height']):
        for y in range(image['width']): 
            color = get_pixel(image, x, y) 
            newcolor = kernel_calc(color, x, y, kernel)
            set_pixel(result, newcolor)
    return result



def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    def rules(c):
        if c < 0:
            # clip negative pixel values to 0  
            c = 0
        elif c > 255:
            # clip values greater than 255 to 255
            c = 255
        else:
            # ensure all values in the image are integers
            c = round(c)
        return c

    return apply_per_pixel(image, rules)


# FILTERS

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """

    # create a representation for the appropriate n-by-n kernel 
    kernel = [[1/(n**2)] * n for _ in range(n)]

    # compute the correlation of the input image with that kernel
    result = correlate(image, kernel)

    # make sure that the output is a valid image 
    result = round_and_clip_image(result)

    return result 


def sharpened(image, n):
    """
    Return a new image representing the result of applying a sharpen effect (with
    kernel size n) to the input image.
    """
    # compute 'minus blurred version' kernel
    kernel = [[-1/(n**2)] * n for _ in range(n)]

    # find the center pixel of kernel 
    k_center = (n-1)//2

    # this operation is as if adding 2 identity kernel to 'minus blurred version' kernel
    kernel[k_center][k_center] += 2 

    # then compute the correlation of the input image with the computed kernel
    result = correlate(image, kernel)

    # make sure that the output is a valid image 
    result = round_and_clip_image(result)

    return result 


def edges(image):
    """
    Detect the edges in a given image. 
    Return a new image resulting from a series of operations where the edges are emphasized. 
    """
    # kernel Kx 
    Kx=[[-1,0,1],
        [-2,0,2],
        [-1,0,1]]
    # kernel Ky 
    Ky=[[-1,-2,-1],
        [0, 0, 0],
        [1, 2, 1]]
    # compute Ox and Oy by correlating the input with Kx and Ky respectively 
    Ox = correlate(image, Kx)
    Oy = correlate(image, Ky)

    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }

    # for y in Oy['pixels']:
    #     set_pixel(result, y)

    # each pixel of the output is the square root of the sum of squares of corresponding pixels in Ox and Oy
    for x, y in zip(Ox['pixels'], Oy['pixels']):
        Oxy = round((x**2 + y**2)**(1/2)) #round(math.sqrt(x**2 + y**2))
        set_pixel(result, Oxy)

    result = round_and_clip_image(result)
    return result

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    
    bluegill = load_image('test_images/bluegill.png')
    pigbird = load_image('test_images/pigbird.png')
    cat = load_image('test_images/cat.png')
    python = load_image('test_images/python.png')
    construct = load_image('test_images/construct.png')
    centered_pixel = load_image('test_images/centered_pixel.png')
    
    # save_image(inverted(bluegill), 'test_images/bluegill_invert.png')
    # save_image(kernel(pigbird, nine_by_nine_kernel), 'test_images/pigbird_nine_by_nine.png')
    # save_image(blurred(cat, 5), 'test_images/cat_blurred_1.png')
    # save_image(sharpened(python, 11), 'test_images/python_sharpened.png')
    save_image(edges(construct), 'test_images/construct_edges.png')

    # save_image(blurred(centered_pixel, 3), 'test_images/centered_pixel_blurred.png')
    # save_image(edges(centered_pixel), 'test_images/centered_pixel_edges.png')
