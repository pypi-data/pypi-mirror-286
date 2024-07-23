import cv2
import pickle


def read_calibration_data(calibration_file=None):
    """
    Read calibration data from a file.

    Args:
        calibration_file (str, optional): Path to the calibration file. If not provided, the default file name 'camera_calibration.p' will be used.

    Returns:
        tuple: A tuple containing the camera matrix (mtx) and distortion coefficients (dist).
    """
    if calibration_file is None:
        calibration_file = 'camera_calibration.p'
        
    with open(calibration_file, 'rb') as f:
        mtx, dist = pickle.load(f)
    
    return mtx, dist


def undistort(img, mtx=None, dist=None):
    """
    Undistorts an image using camera calibration parameters.

    Args:
        img (numpy.ndarray): The input image to be undistorted.
        mtx (numpy.ndarray, optional): The camera matrix. If not provided, it will be read from calibration data.
        dist (numpy.ndarray, optional): The distortion coefficients. If not provided, they will be read from calibration data.

    Returns:
        numpy.ndarray: The undistorted image.

    """
    if mtx is None or dist is None:
        mtx, dist = read_calibration_data()
        
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    return dst


