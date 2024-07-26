import numpy as np
import cv2 


def square(img, fov, focal_length, pixel_size):
    """
    Draws a square on the input image.

    Args:
        img (numpy.ndarray): The input image.
        fov (float): The field of view in degrees.
        focal_length (float): The focal length of the camera in mm.
        pixel_size (float): The size of each pixel in the camera sensor in mm.

    Returns:
        numpy.ndarray: The image with a square drawn on it.
    """
    assert isinstance(img, np.ndarray), 'img must be a numpy array.'
    assert isinstance(fov, (int, float)), 'fov must be an integer or float.'
    assert isinstance(focal_length, (int, float)), 'focal_length must be an integer or float.'
    assert isinstance(pixel_size, (int, float)), 'pixel_size must be an integer or float.'
    
    h, w = img.shape[:2]
    sensor_size = 2 * np.tan(np.deg2rad(fov)/2) * focal_length
    pixel_density = 1/pixel_size
    pixel = int(sensor_size * pixel_density)
    cv2.rectangle(img, (int(w/2 - pixel/2), int(h/2 - pixel/2)), (int(w/2 + pixel/2), int(h/2 + pixel/2)), (0, 255, 0), 2)  
    
    
    return img


def divide(img, fov, focal_length, pixel_size, portions):
    """
    Divides the input image into portions and draws rectangles on each portion.

    Parameters:
    img (numpy.ndarray): The input image.
    fov (float): The field of view in degrees.
    focal_length (float): The focal length of the camera in mm.
    pixel_size (float): The size of each pixel in the image.
    portions (int): The number of portions to divide the image into.

    Returns:
    numpy.ndarray: The image with rectangles drawn on each portion.
    """
    assert isinstance(img, np.ndarray), 'img must be a numpy array.'
    assert isinstance(fov, (int, float)), 'fov must be an integer or float.'
    assert isinstance(focal_length, (int, float)), 'focal_length must be an integer or float.'
    assert isinstance(pixel_size, (int, float)), 'pixel_size must be an integer or float.'
    assert isinstance(portions, int), 'portions must be an integer.'
    
    h, w = img.shape[:2]
    sensor_size = 2 * np.tan(np.deg2rad(fov)/2) * focal_length
    pixel_density = 1/pixel_size
    pixel = int(sensor_size * pixel_density)
    for i in range(portions):
        for j in range(portions):
            cv2.rectangle(img, (int(w/2 - pixel/2 + i*pixel/portions), int(h/2 - pixel/2 + j*pixel/portions)), (int(w/2 - pixel/2 + (i+1)*pixel/portions), int(h/2 - pixel/2 + (j+1)*pixel/portions)), (0, 255, 0), 2)

    return img

