import os
import cv2


def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
    define a list to contain all the (image, label) tuple.
    """
    dataset = list()
    for file in os.listdir(dataPath + "/face"):
        # read all face images and label 1
        img = cv2.imread(f"{dataPath}/face/{file}", cv2.IMREAD_GRAYSCALE)
        dataset.append((img, 1))
    for file in os.listdir(dataPath + "/non-face"):
        # read all non-face images and label 0
        img = cv2.imread(f"{dataPath}/non-face/{file}", cv2.IMREAD_GRAYSCALE)
        dataset.append((img, 0))
    # End your code (Part 1)
    return dataset
