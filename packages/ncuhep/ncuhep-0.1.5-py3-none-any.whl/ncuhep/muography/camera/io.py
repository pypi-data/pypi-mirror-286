import cv2


def save(image, path):
    """
    Save the given image to the specified path.

    Args:
        image: The image to be saved.
        path: The path where the image will be saved.

    Returns:
        None
    """
    cv2.imwrite(path, image)
    
    
def read(path):
    """
    Reads an image from the specified path using OpenCV.

    Args:
        path (str): The path to the image file.

    Returns:
        numpy.ndarray: The image data as a NumPy array.

    """
    return cv2.imread(path)


def show(image, title='Image'):
    """
    Displays the given image in a window with the specified title.

    Parameters:
    - image: The image to be displayed.
    - title: The title of the window (default is 'Image').
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    