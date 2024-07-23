"""OpenCV image writer"""
import cv2
import numpy as np


def image_write(file: np.ndarray, path: str):
    """OpenCV image writer"""
    res = cv2.imwrite(path, file[..., ::-1])
    assert res is not None, f"Image {file.shape} could not be saved to '{path}'"
