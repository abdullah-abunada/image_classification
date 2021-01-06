from skimage.transform import resize
from skimage import feature
import cv2


def get_hog_features(file):
    # 1: read image file
    image = cv2.imread(file)
    # 2: convert image to grayscale color
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 3: resize the image to be (90* 90) RGP
    image = resize(image, (90, 90))
    # 4: extract image features using hog
    (hog, hog_image) = feature.hog(image, orientations=9,
                                   pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                   block_norm='L2-Hys', visualize=True, transform_sqrt=True)
    # 5: return hog features
    return hog_image


def label_decode(label):
    if label == 0:
        return 'Daffodil'
    elif label == 1:
        return 'Daisy'
    elif label == 2:
        return 'Iris'
    elif label == 3:
        return 'Sunflower'
    elif label == 4:
        return 'Windflower'
    else:
        return 'unknown'
