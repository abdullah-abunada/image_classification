import glob
from skimage.transform import resize
from skimage import feature
import cv2
import pandas as pd
import json
import base64

folders = ['Daffodil', 'Daisy', 'Iris', 'Sunflower', 'Windflower']
# crate new dataframe
df = pd.DataFrame(columns=['image', 'hog' 'label'])
# store images and there features in dataset
for folder in folders:
    path = './row_data/' + folder + '/*.jpg'
    # get only the jpg images
    files = glob.glob(path)
    for file in files:
        # 1: read the image
        image = cv2.imread(file)
        # 2: convert image to RGP color
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 3: resize the image to be (90* 90) RGP
        image = resize(image, (90, 90))
        # 4: convert to grayscale
        #g_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # 5: extract image features using hog
        (hog, hog_image) = feature.hog(image, orientations=9,
                                       pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                       block_norm='L2-Hys', visualize=True, transform_sqrt=True)
        #6: append data to dataframe using the "dictionary way"
        data = json.dumps(
            [str(hog_image.dtype), base64.encodebytes(hog_image.tobytes()).decode("utf-8"), hog_image.shape])
        original_image = json.dumps(
            [str(image.dtype), base64.encodebytes(image.tobytes()).decode("utf-8"), image.shape])
        image_row = {'image': original_image, 'hog': data, 'label': folder}
        df = df.append(image_row, ignore_index=True)

# save our dataframe to csv file
df.to_csv('./dataset/flowers_features_json.csv')
