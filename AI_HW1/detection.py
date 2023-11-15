import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    read in all images and the position to be detected, resize it , and classify it.
    """
    # get all data in a list, for the convenience when processing it
    data = []
    with open(dataPath) as f:
        t = f.readline()
        while t != '':
            file, count = t.split()
            # record all rectangles to be classified
            rect = []
            for i in range(int(count)):
                x, y, w, h = [int(k) for k in f.readline().split()]
                rect.append((x, y, w, h))
            # append (filename, rectangles) tuple to data list
            data.append((file, rect))
            t = f.readline()

    # show all images in one plot
    fig, axs = plt.subplots(2, 2)

    for i, file in enumerate(data):
        # read images and convert to gray (to classify) and BGR(for matplotlib)
        img = cv2.imread("data/detect/" + file[0])
        imgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        axs[i // 2][i % 2].axis('off')
        axs[i // 2][i % 2].imshow(imgb)
        axs[i // 2][i % 2].set_title(file[0])
        for rect in file[1]:
            x, y, w, h = rect
            # for each rectangle, get the sub image and resize it to 19x19
            sub = gray[y:y+h, x:x+w]
            sub = cv2.resize(sub, (19, 19), cv2.INTER_AREA)
            # use a patch to:
            # draw a green box if the rectangle is positively classified,
            # red box if it is negatively classified.
            if clf.classify(sub):
                patch = patches.Rectangle((x, y), w, h, edgecolor='green', facecolor='none')
            else:
                patch = patches.Rectangle((x, y), w, h, edgecolor='red', facecolor='none')
            axs[i // 2][i % 2].add_patch(patch)

    # show the results
    plt.show()
    # End your code (Part 4)
