#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


# VARIOUS FILTERS

def get_pixel(image, x, y):

    width = image['width']
    height = image['height']
    if x > width - 1:
        x = width - 1
    if x < 0:
        x = 0
    if y > height - 1:
        y = height - 1
    if y <0:
        y = 0
    return image['pixels'][(width * y) + x]


def set_pixel(image, x, y, c):
    image['pixels'][(y*image['width']) + x] = c


def apply_per_pixel(image, func):
    result = {'height': image['height'], 'width': image['width'], 'pixels': [0]*len(image['pixels'])}
    for x_coord in range(image['width']):
        for y_coord in range(image['height']):
            color = get_pixel(image, x_coord, y_coord)
            newcolor = func(color)
            set_pixel(result, x_coord, y_coord, newcolor)
    return result

def inverted(image): 
    return apply_per_pixel(image, lambda c: (255-c))

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    Kernel: 2-d array or list of lists represents the kernel being applied
    """
    height = image['height']
    width = image['width']
    result = {'height': height, 'width' : width, 'pixels' : [0]*len(image['pixels'])}
    kernel_size = len(kernel)//2
    
    for x_coord in range(width):
        
        for y_coord in range(height):
            
            correlated_value = 0
            
            for y_coord1 in range(len(kernel)):
                
                for x_coord1 in range(len(kernel[y_coord1])):
                    
                    x_coord2 = x_coord - kernel_size + x_coord1
                    
                    y_coord2 = y_coord - kernel_size + y_coord1
                    
                    correlated_value = (get_pixel(image, x_coord2, y_coord2) * kernel[y_coord1][x_coord1]) + correlated_value
                    
            set_pixel(result, x_coord, y_coord, correlated_value)
            
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
    for i in range(len(image['pixels'])):
        
        image['pixels'][i] = int(round(image['pixels'][i]))
        
        if image['pixels'][i] < 0:
            
            image['pixels'][i] = 0
            
        elif image['pixels'][i] > 255:
            
            image['pixels'][i] = 255
            


# FILTERS


def box_blur(n):
    """
    Given a kernel size, n, creates the "box blur" matrix to be applied/correlated to any image requiring
    it--Returns a matrix/list of lists with the appropriate values
    """
    kernel = []
    
    for i in range(n):
        
        row = []
        
        for j in range(n):
        
            row.append(1/n**2)
            
        kernel.append(row)
        
    return kernel


def embossed(color_image):
    """
    Return a new image representing the result of applying a specified kernel (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output, and it should show the highllight/
    shadows on the image contour.
    """
    kernel = [[0, 1, 0], [0, 0, 0], [0, -1, 0]]
    image_list = split_color_image(color_image)
    red = correlate(image_list[0], kernel)
    green = correlate(image_list[1], kernel)
    blue = correlate(image_list[2], kernel)
    result = recombine_color_image(red, green, blue)
    return result


def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    result = correlate(image, box_blur(n))
    
    round_and_clip_image(result)
    
    return result



def sharpened(image, n):
    """
    Returns a new image representing the result of applying a box blur and subtracting
    the resulting values from twice the pixel value in the original image 
    *Add parameter information and what the function returns*
    """
    
    height = image['height']
    width = image['width']
    result = {'height': height, 'width' : width, 'pixels' : [0]*len(image['pixels'])}
    blurred = correlate(image, box_blur(n))
    
    
    for x_coord in range(width):
        
        for y_coord in range(height):
            
            c = 2 * get_pixel(image, x_coord, y_coord) - get_pixel(blurred, x_coord, y_coord)
            
            set_pixel(result, x_coord, y_coord, c)
            
    round_and_clip_image(result)
    
    return result


def edges(image):
    """
    Returns a newimage representing the result of correlating the specified kernel
    to the actual image inputted in order to detect an edge and return a new image
    with all of the "edges" identified
    """
    height = image['height']
    
    width = image['width']
    
    result = {'height': height, 'width' : width, 'pixels' : [0]*len(image['pixels'])}
    
    kernel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    kernel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    
    O_x = correlate(image, kernel_x)
    O_y = correlate(image, kernel_y)
    
    for x_coord in range(width):
        
        for y_coord in range(height):
            
            c = ((get_pixel(O_x, x_coord, y_coord))**2 + (get_pixel(O_y, x_coord, y_coord))**2)**0.5
            
            set_pixel(result, x_coord, y_coord, c)
            
    round_and_clip_image(result)
    return result


def split_color_image(color_image):
    """
    Given an image in color, splits the image into its respective 3 greyscaled 
    images based on the intensity given for each color in all of the pixels. It
    returns a list of all three "split" color images.
    """
    height = color_image['height']
    width = color_image['width']
    result_red = {'height': height, 'width' : width, 'pixels' : [0]*len(color_image['pixels'])}
    result_green = {'height': height, 'width' : width, 'pixels' : [0]*len(color_image['pixels'])}
    result_blue = {'height': height, 'width' : width, 'pixels' : [0]*len(color_image['pixels'])}
    for x_coord in range(width):
        for y_coord in range(height):
            red = get_pixel(color_image, x_coord, y_coord)[0]
            green = get_pixel(color_image, x_coord, y_coord)[1]
            blue = get_pixel(color_image, x_coord, y_coord)[2]
            result_red['pixels'][(y_coord*width) + x_coord] = red
            result_green['pixels'][(y_coord*width) + x_coord] = green
            result_blue['pixels'][(y_coord*width) + x_coord] = blue
    return [result_red, result_green, result_blue]


def recombine_color_image(red_image, green_image, blue_image):
    """
    Given 3 greyscaled images, all of whose pixels represent color intensities 
    for red, green, and blue colors respectively, returns a color image with all
    inputted values assigned to their respective spots within the final image's
    pixels.
    """
    height = red_image['height']
    width = red_image['width']
    result = {'height': height, 'width' : width, 'pixels' : [0]*len(red_image['pixels'])}
    for x_coord in range(width):
        for y_coord in range(height):
            red_value = get_pixel(red_image, x_coord, y_coord)
            green_value = get_pixel(green_image, x_coord, y_coord)
            blue_value = get_pixel(blue_image, x_coord, y_coord)
            pixel_tuple = (red_value, green_value, blue_value)
            result['pixels'][(y_coord*red_image['width']) + x_coord] = pixel_tuple
    return result


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def new_color_filter(color_image):
        greyscaled_images = split_color_image(color_image)
        red_image = filt(greyscaled_images[0])
        green_image = filt(greyscaled_images[1])
        blue_image = filt(greyscaled_images[2])
        result = recombine_color_image(red_image, green_image, blue_image)
        return result        
    return new_color_filter


def make_blur_filter(n):
    """
    Given a parameter n for kernel/box blur size (a single parameter), returns
    a function/filter that blurs a color image when inputted into the
    color_filter_from_greyscale_filter.
    """
    def blur(image):
        return blurred(image,n)
    return blur


def make_sharpen_filter(n):
    """
    Given a parameter n for kernel/box blur size (a single parameter), returns
    a function/filter that sharpens a color image when inputted into the
    color_filter_from_greyscale_filter.
    """
    def sharp(image):
        return sharpened(image,n)
    return sharp


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def final_filter(image):
        while len(filters) > 0:
            removed_filter = filters.pop(0)
            image = removed_filter(image)
        return image
    return final_filter


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    grey_image = greyscale_image_from_color_image(image)
    energy = compute_energy(grey_image)
    cem = cumulative_energy_map(energy)
    while ncols > 0:
        seam = minimum_energy_seam(cem)
        image = image_without_seam(image, seam)
        grey_image = greyscale_image_from_color_image(image) #recalculates the new CEM to be used in the next loop (314-317)
        energy = compute_energy(grey_image)
        cem = cumulative_energy_map(energy)
        ncols = ncols - 1
    return image


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    height = image['height']
    width = image['width']
    result = {'height': height, 'width' : width, 'pixels' : [0]*len(image['pixels'])}
    for x_coord in range(width):
        for y_coord in range(height):
            red_value = get_pixel(image, x_coord, y_coord)[0] * 0.299
            green_value = get_pixel(image, x_coord, y_coord)[1] * 0.587
            blue_value = get_pixel(image, x_coord, y_coord)[2] * 0.114
            grey_value = round(red_value + green_value + blue_value)
            set_pixel(result, x_coord, y_coord, grey_value)
    return result
    

def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy function),
    computes a "cumulative energy map" as described in the lab 2 writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    height = energy['height']
    width = energy['width']
    result = {'height': height, 'width' : width, 'pixels' : energy['pixels'].copy()}
    for y_coord in range(1, height): #excludes the top row, starts at row 1
        for x_coord in range(width):
            added_value = min(get_pixel(result, x_coord - 1, y_coord -1), get_pixel(result, x_coord, y_coord-1), get_pixel(result, x_coord+1, y_coord-1))+ get_pixel(energy, x_coord, y_coord)
            set_pixel(result, x_coord, y_coord, added_value)
    return result


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    height = cem['height']
    width = cem['width']
    path = [] #contains tuple of x and y coordinates for each element of seam
    path_index = -1 #keeps track of which element is being looked at
    for y in range(height - 1, -1, -1):
        start = width*y
        end = width*y + width
        row = cem['pixels'][start:end]
        if path_index == -1:
            min_num = min(row)
            x = row.index(min_num)
            path.append((x,y))
        else:
            x_coord = path[path_index][0]
            if x_coord == 0:
                min_num = min((get_pixel(cem, x_coord, y), x_coord), (get_pixel(cem, x_coord+1, y), x_coord +1)) #gets the index of the minimum in the context of the "row"
                x = min_num[1]
            elif x_coord == width - 1:
                min_num = min((get_pixel(cem, x_coord - 1, y), x_coord - 1), (get_pixel(cem, x_coord, y), x_coord))
                x = min_num[1]
            else:
                min_num = min((get_pixel(cem, x_coord - 1, y), x_coord -1), (get_pixel(cem, x_coord, y), x_coord), (get_pixel(cem, x_coord+1, y), x_coord +1))
                x = min_num[1]
            path.append((x,y))
        path_index = path_index + 1
    final_seam = [] #calculates the indexes from the "path list" created above
    for tup in path:
        index = (width*tup[1]) + tup[0]
        final_seam.append(index)
    return final_seam
                

def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    height = image['height']
    width = image['width']
    pixels = image['pixels'].copy()
    for index in seam:
        del pixels[index]
    new_image = {'height': height, 'width' : width -1, 'pixels' : pixels}
    return new_image


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES
    
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


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # pass
    image = load_color_image('test_images/construct.png')
    new_image = embossed(image)
    save_color_image(new_image, 'test_images/construct2.png', mode = 'PNG')
