import numpy as np
import cv2
import glob
import pickle


def calibrate(image_path, checkerboard_dim, save_path=None, visualize=False):
    """
    Calibrates the camera using a set of images of a checkerboard pattern.

    Args:
        image_path (str): The path to the directory containing the checkerboard images.
        checkerboard_dim (tuple): The dimensions of the checkerboard pattern (rows, columns).
        save_path (str, optional): The path to save the camera calibration parameters. If not provided, the parameters will be saved to 'camera_calibration.p' in the current directory. Defaults to None.
        visualize (bool, optional): Whether to visualize the detected corners on the images. Defaults to False.

    Returns:
        tuple: A tuple containing the camera matrix (mtx) and distortion coefficients (dist).
    """
    
    assert isinstance(image_path, str), 'image_path must be a string.'
    assert isinstance(checkerboard_dim, tuple), 'checkerboard_dim must be a tuple.'
    assert len(checkerboard_dim) == 2, 'checkerboard_dim must be a tuple of length 2.'
    assert isinstance(checkerboard_dim[0], int) and isinstance(checkerboard_dim[1], int), 'checkerboard_dim must contain integers.'
    assert isinstance(save_path, (str, type(None))), 'save_path must be a string or None.'
    assert isinstance(visualize, bool), 'visualize must be a boolean.'
    
    objp = np.zeros((checkerboard_dim[0]*checkerboard_dim[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:checkerboard_dim[0],0:checkerboard_dim[1]].T.reshape(-1,2)
    
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    
    images = glob.glob(image_path)
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        print(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_dim, None)
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            if visualize:
                cv2.drawChessboardCorners(img, checkerboard_dim, corners, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)
    cv2.destroyAllWindows()
    
    img = cv2.imread(images[0])
    img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

    if save_path is not None:
        with open(save_path, 'wb') as f:
            pickle.dump([mtx, dist], f)
    else:
        with open('camera_calibration.p', 'wb') as f:
            pickle.dump([mtx, dist], f)
            
    return mtx, dist
