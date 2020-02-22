from scipy import cluster
import matplotlib.pyplot as plt
import pandas
import math
import colorsys
from color_detect.utils import create_color_palette, rgb_list_to_hex


def step(r, g, b, repititions=1):
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h2 = int(h * repititions)
    lum2 = int(lum * repititions)
    v2 = int(v * repititions)

    if h2 % 2 == 1:
        v2 = repititions - v2
        lum = repititions - lum

    return (h2, lum, v2)


def get_dominant_colors(input_file, num_colors=4):
    img = plt.imread(input_file)

    red, green, blue = [], [], []
    for line in img:
        for pixel in line:
            r, g, b = pixel
            red.append(r)
            green.append(g)
            blue.append(b)

    df = pandas.DataFrame({
        'red': red,
        'green': green,
        'blue': blue
    })

    df['standardized_red'] = cluster.vq.whiten(df['red'])
    df['standardized_green'] = cluster.vq.whiten(df['green'])
    df['standardized_blue'] = cluster.vq.whiten(df['blue'])

    color_pallete, distortion = cluster.vq.kmeans(df[['standardized_red', 'standardized_green', 'standardized_blue']],
                                                  num_colors)
    colors = []
    red_std, green_std, blue_std = df[['red', 'green', 'blue']].std()
    for color in color_pallete:
        scaled_red, scaled_green, scaled_blue = color
        colors.append((
            math.ceil(scaled_red * red_std),
            math.ceil(scaled_green * green_std),
            math.ceil(scaled_blue * blue_std)
        ))

    colors.sort(key=lambda x: step(x[0], x[1], x[2], 8))
    # return rgb_list_to_hex(colors)
    return colors


if __name__ == '__main__':
    img_name = './shoe1.jpg'
    colors = get_dominant_colors(img_name)
    # colors = ['#d3cec7', '#f2f2f2', '#72757a', '#3a3b40']
    create_color_palette('./test.jpg', colors)
