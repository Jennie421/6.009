#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


# GRAYSCALE FILTERS
def get_pixel(image, x, y):
    """
    Return the color of pixel at position (x, y) of a given image. 
    """
    index = x * image['width'] + y
    return image['pixels'][index]

def get_possible_pixel(image, x, y):
    """
    Return the color of pixel at position (x, y) of a given image. 
    """
    if 0 <= x < image['height'] and 0 <= y < image['width']:
        index = x * image['width'] + y
        return image['pixels'][index]
    else:
        return None

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

    # each pixel of the output is the square root of the sum of squares of corresponding pixels in Ox and Oy
    for x, y in zip(Ox['pixels'], Oy['pixels']):
        Oxy = round(math.sqrt(x**2 + y**2))
        set_pixel(result, Oxy)

    result = round_and_clip_image(result)
    return result


# HELPER FUNCTIONS 


def separate(color_im):
    """
    Split a given color image into three separate grey scale images.
    Return a list of three separated image in the order of [R, G, B]. 
    """
    height = color_im['height']
    width = color_im['width']
    red, green, blue = [], [], [] # store the pixels of each color 
    
    for i in color_im['pixels']:
        red.append(i[0])
        green.append(i[1])
        blue.append(i[2])
   
    red_im = {
        'height': height, 
        'width': width, 
        'pixels': red, 
    }
    
    green_im = {
        'height': height, 
        'width': width, 
        'pixels': green, 
    }

    blue_im = {
        'height': height, 
        'width': width, 
        'pixels': blue, 
    }

    separated = [red_im, green_im, blue_im]
    return separated 



def combine(red_im, green_im, blue_im):
    """
    Combine three greyscale images into a single new color image. 
    Return a new combined image. 
    """
    combined = []
    for red, green, blue in zip(red_im['pixels'], green_im['pixels'], blue_im['pixels']):
        color_pixel = (red, green, blue)
        combined.append(color_pixel)

    color_im = {
        'height': red_im['height'],
        'width': red_im['width'], 
        'pixels': combined, 
    }
    return color_im 


# VARIOUS FILTERS

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filt(color_im):
        separated = separate(color_im)

        # apply filter on each separated images 
        red_filt = filt(separated[0]) 
        green_filt = filt(separated[1])
        blue_filt = filt(separated[2])

        combined = combine(red_filt, green_filt, blue_filt)
        return combined

    return color_filt


def make_blur_filter(n):
    """
    Takes the parameter n and returns a blur filter which takes a single image as argument
    """
    def blur_filter(image):
        return blurred(image, n)

    return blur_filter


def make_sharpen_filter(n):
    """
    Takes the parameter n and returns a sharpen filter which takes a single image as argument
    """
    def sharp_filter(image):
        return sharpened(image, n)

    return sharp_filter


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def cascade (image):
        new = dict(image)
        for f in filters:
            new = f(new)
        return new
    return cascade 



# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    new = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'][:],
    }
    
    i = 0
    while i < ncols: # befoer enough number of columns are removed
        grey = greyscale_image_from_color_image(new)
        energy = compute_energy(grey)
        cem = cumulative_energy_map(energy)
        seam = minimum_energy_seam(cem)
        new = image_without_seam(new, seam)
        new['width'] -= 1
        i+=1

    return new


# Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    grey = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    separated = separate(image)
    for r, g, b in zip(separated[0]['pixels'], separated[1]['pixels'], separated[2]['pixels']):
        g = round(.299*r + .587*g + .114*b)
        set_pixel(grey, g)
    return grey


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    energy = edges(grey)
    return energy


def adjacent_min(im, x, y):
    """
    Takes a image and a x-y location of a pixel, 
    returns the minimum value and index of adjacent pixels in the row above in form of (value, indix)
    """
    if x == 0:
        # if is the top row
        return None
    
    adjacent = [] # stores the value and index of adjacent pixels in the row above
    if 0 <= y - 1 < im['width']:
        adjacent.append((get_pixel(im, x - 1, y - 1), y - 1)) # include the upper left pixel 
    if 0 <= y < im['width']:
        adjacent.append((get_pixel(im, x - 1, y), y)) # include the upper pixel 
    if 0 <= y + 1 < im['width']:
        adjacent.append((get_pixel(im, x - 1, y + 1), y + 1)) # include the upper right pixel

    # for each pair in `adjacent`, compare against their values `pair[0]`
    # then return the pair with minimum value.
    return min(*adjacent, key=lambda pair: pair[0])


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    cem = {
        'height': energy['height'],
        'width': energy['width'],
        'pixels': energy['pixels'][:],
    }

    for x in range(cem['height']):
        for y in range(cem['width']): 
            adj_value = adjacent_min(cem, x, y)
            if adj_value: # if have adjacent pixels 
                # set the value of current location, added to the minimum of 
                # the cumulative energies from the "adjacent" pixels in the row above
                current = get_pixel(cem, x, y)
                new = current + adj_value[0]
                index = x * cem['width'] + y 
                cem['pixels'][index] = new
    return cem


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    seam = [] # store indices need to be removed

    # Find the minimum value pixel in the bottom row of the cumulative energy map is located.
    x = cem['height'] - 1 # locate bottom row
    min_idx = x * cem['width']
    min_y = 0
    min_pixel = get_pixel(cem, x, 0)
    for y in range(1, cem['width']): 
        current = get_pixel(cem, x, y)
        if current < min_pixel: 
            min_pixel = current
            min_idx = x * cem['width'] + y
            min_y = y

    seam.append(min_idx)

    # The seam is then traced back up to the top row of the cumulative energy map 
    # by following the adjacent pixels with the smallest cumulative energies.  
    while x > 0:
        min_y = adjacent_min(cem, x, min_y)[1] # get the index of min adjacent pixel 
        x -= 1 # move to one row above 
        seam.append(x * cem['width'] + min_y) 

    return seam


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    carved = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    
    for i in range(len(image['pixels'])):
        if i not in seam:
            set_pixel(carved, image['pixels'][i])
    return carved



# SELF DESIGN
def image_with_seam(image, seam):
    added = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    
    for i in range(len(image['pixels'])):
        if i in seam:
            set_pixel(added, image['pixels'][i])
            set_pixel(added, image['pixels'][i])
        else:
            set_pixel(added, image['pixels'][i])
    return added


def seam_adding(image, ncols):
    """
    Starting from the given image, add ncols (an integer) columns from the image.
    """
    new = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'][:],
    }
    
    i = 0
    while i < ncols: # befoer enough number of columns are added
        grey = greyscale_image_from_color_image(new)
        energy = compute_energy(grey)
        cem = cumulative_energy_map(energy)
        seam = minimum_energy_seam(cem)
        new = image_with_seam(new, seam)
        new['width'] += 1 # inc width
        i+=1

    return new


# for transparent 
def seam_list(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    new = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'][:],
    }
    
    width = image['width']
    seam_total = []
    i = 0
    while i < ncols: # befoer enough number of columns are removed
        grey = greyscale_image_from_color_image(new)
        energy = compute_energy(grey)
        cem = cumulative_energy_map(energy)
        seam = minimum_energy_seam(cem) # seam = list of indcies to remove 
        
        for idx in seam:
            seam_total.append(idx + i * width) 
            
        new = image_without_seam(new, seam)
        new['width'] -= 1
        i+=1

    return seam_total



def overlay(top_im, bottom_im, bx, by, colns): 
    """
    Parameters: 
        * top_im: the image that should be laid on top  
        * bottom_im: the image that should be laid on bottom
        * bx, by: a coordinate in bottom image, where the top image should be placed at
    Returns:
        a new image that represents the onerlay of two given images. 
    """
    # check for valid imput 
    if bx > bottom_im['height'] or by > bottom_im['width']:
        print("Invalid input: the bottom image has height", bottom_im['height'], "and width", bottom_im['width'])
        return None

    # if bottom image is smaller, extend its borders using seam_adding()
    if bottom_im['width'] < top_im['width']:
        # extend width 
        ncols = top_im['height'] - bottom_im['height']
        bottom_im = seam_adding(bottom_im, ncols)


    result = {
        'height': bottom_im['height'], 
        'width': bottom_im['width'], 
        'pixels': [], 
    }

    # locate the position of top image in bottom image 
    top_height_range = range(bx, bx + top_im['height'])
    top_width_range = range(by, by + top_im['width'])


    # make transparent 
    idx_remove = seam_list(top_im, colns)

    # overylay two images
    for x in range(bottom_im['height']):
        for y in range(bottom_im['width']):
            bottom = get_pixel(bottom_im, x, y)

            if x in top_height_range and y in top_width_range:
                tx = x - bx # x location of top image
                ty = y - by # y location of top image 
                t_index = tx * top_im['width'] + ty 

                if t_index not in idx_remove:
                    top = get_pixel(top_im, tx, ty)
                    set_pixel(result, top)
                else: 
                    set_pixel(result, bottom)
            else:
                set_pixel(result, bottom)

    return result



# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
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


def save_greyscale_image(image, filename, mode='PNG'):
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

    # load image
    # bluegill = load_color_image('test_images/bluegill.png')
    # pigbird = load_color_image('test_images/pigbird.png')
    # cat = load_color_image('test_images/cat.png')
    # python = load_color_image('test_images/python.png')
    # construct = load_color_image('test_images/construct.png')
    # pixel = load_color_image('test_images/centered_pixel.png')
    # sparrowchick = load_color_image('test_images/sparrowchick.png')
    # frog = load_color_image('test_images/frog.png')
    smallfrog = load_color_image('test_images/smallfrog.png')
    twocats = load_color_image('test_images/twocats.png')
    # pattern = load_color_image('test_images/pattern.png')
    tree = load_color_image('test_images/tree.png')
    tree2 = load_color_image('test_images/tree2.png')
    tree3 = load_color_image('test_images/tree3.png')
    whitecat = load_color_image('test_images/whitecat.png')
    

    # My design
    save_color_image(overlay(smallfrog, twocats, 50, 20, 0), 'frog & twocats.png')
    # save_color_image(overlay(twocats, tree3, 1200, 300, 50), 'twocats & tree3.png')
    # save_color_image(overlay(twocats, tree2, 200, 200, 2), 'twocats & tree2 & transparent.png')
    # save_color_image(overlay(twocats, tree2, 200, 200, 0), 'twocats & tree2.png')
    # save_color_image(seam_adding(tree, 100), 'twocats & tree2.png')
    # save_color_image(overlay(twocats, tree2, 200, 200, 0), 'twocats & tree2.png')

    save_color_image(overlay(whitecat, tree2, 200, 0, 0), 'whitecat & tree2 & transparent.png')


    # 4.1 
    # color_inverted = color_filter_from_greyscale_filter(inverted) # create color invert filter
    # cat_inverted = color_inverted(cat)
    # save_color_image(cat_inverted, 'test_images/cat_inverted.png')
    
    # 4.3
    # blur_filter_3 = make_blur_filter(3) # create color blur filter with n = 3
    # color_blur_filter_3 = color_filter_from_greyscale_filter(blur_filter_3) # create color invert filter
    # save_color_image(color_blur_filter_3(cat), 'test_images/cat_blur_3.png')

    # python_blur_9 = make_blur_filter(9)(python) # blur python with n = 9 
    # save_color_image(python_blur_9, 'test_images/python_blur_9.png')
    # sparrowchick_sharp_7 = make_sharpen_filter(7)(sparrowchick) # sharpen sparrowchick with n = 7
    # save_color_image(sparrowchick_sharp_7, 'test_images/sparrowchick_sharp_7.png')  
    
    # 5.1
    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # pixel_cascade = filt(pixel)
    # save_color_image(pixel_cascade, 'test_images/centered_pixel_cascade.png')
    # frog_cascade = filt(frog)
    # save_color_image(frog_cascade, 'test_images/frog_cascade.png')

    #6.5
    # c = seam_carving(twocats, 100)
    # save_color_image(c, 'test_images/twocats_carved.png')