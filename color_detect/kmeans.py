from collections import Counter

import cv2
from sklearn.cluster import KMeans
import numpy as np
from color_detect.utils import create_color_palette, hsv2rgb


def divide_100(n):
    return n / 100


def get_dominant_colors(input_file, num_colors=4):
    image = cv2.imread(input_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # ignore white colors
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    # black: [0, 0, 200] [180, 255, 255]
    # white: [0, 0, 200] [180, 20, 255]
    mask = cv2.inRange(image, low, high)
    img = cv2.bitwise_and(image, image, mask=mask)
    reshaped = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
    kmeans = KMeans(n_clusters=num_colors, n_init=40, max_iter=500)
    # kmeans = KMeans(n_clusters=num_colors+1)
    # result = kmeans.fit_predict(reshaped).cluster_centers_
    # result = result.astype(float).tolist()
    # results = []
    # for cl in result:
    #     cl = list(map(divide_100, cl))
    #     rgb = hsv2rgb(*cl)
    #     if rgb == (0, 0, 0):
    #         continue
    #     results.append(rgb)
    # return results
    k = num_colors + 2
    labels = kmeans.fit_predict(reshaped)
    label_counts = Counter(labels)
    results = []
    for item in label_counts.most_common(k):
        index = item[0]
        result = kmeans.cluster_centers_[index]
        result = result.astype(float).tolist()
        cl = list(map(divide_100, result))
        rgb = hsv2rgb(*cl)
        if rgb == (0, 0, 0):
            continue
        results.append(rgb)
    return results[:num_colors]


if __name__ == '__main__':
    # working directory is parent dir
    img_name = './color_detect/shoe1.jpg'
    colors = get_dominant_colors(img_name)
    print(colors)
    create_color_palette('./test2.jpg', colors)
