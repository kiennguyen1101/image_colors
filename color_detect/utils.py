import colorsys
import math


def create_color_palette(output_file, colors):
    from PIL import Image, ImageDraw
    width, height = 256, 256
    num_colors = len(colors)

    pallete = Image.new('RGB', (width, height), (255, 255, 255))

    single_img_space = math.floor(width / num_colors)
    single_img_offset = math.floor(single_img_space / 14)
    total_offset = single_img_offset * (num_colors + 1)
    single_img_width = math.floor((width - total_offset) / num_colors)
    single_img_space = single_img_width + single_img_offset
    final_img_width = (single_img_width + (width - (single_img_space * num_colors))) - single_img_offset

    x_offset = 0
    for i in range(num_colors):
        color = colors[i]
        if isinstance(colors[i], str):
            color = hex_to_rgb(color)
        if i == num_colors - 1:
            new_img = Image.new('RGB', (final_img_width, height), color)
            pallete.paste(new_img, (x_offset, 0))
        elif i == 0:
            new_img = Image.new('RGB', (single_img_width, height), color)
            pallete.paste(new_img, (single_img_offset, 0))
            x_offset += single_img_space + single_img_offset
        else:
            new_img = Image.new('RGB', (single_img_width, height), color)
            pallete.paste(new_img, (x_offset, 0))
            x_offset += single_img_space + single_img_offset
    pallete.save(output_file)


def rgb_to_hex(hex):
    return '#%02x%02x%02x' % hex


def hex_to_rgb(h):
    if '#' in h:
        h = h.replace('#', '')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_list_to_hex(colors):
    new_colors = []
    for color in colors:
        new_colors.append(rgb_to_hex(tuple(color)))
    return new_colors


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))
