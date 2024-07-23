from typing import Dict

import cv2
from PIL import Image
import numpy as np


def cut_map_grid(image, cut_map_size):
    """
    裁剪图像的一部分。

    参数:
    - image: 要裁剪的原始图像对象（PIL Image）。
    - x: 裁剪区域的左上角x坐标。
    - y: 裁剪区域的左上角y坐标。
    - w: 裁剪区域的宽度。
    - h: 裁剪区域的高度。

    返回:
    - 裁剪后的图像对象（PIL Image）。
    """
    # 裁剪图像
    # 确保image是PIL Image对象
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    # 裁剪图像
    cut_image = image.crop((cut_map_size['x'], cut_map_size['y'], cut_map_size['x'] + cut_map_size['w'],
                            cut_map_size['y'] + cut_map_size['h']))
    return cut_image


# def cut_map_grid(image: Image.Image, cut_map_size: Dict[str, int]) -> Image.Image:
#     # 确保 cut_map_size 是包含 'x', 'y', 'w', 'h' 的字典
#     cut_image = image.crop((
#         cut_map_size['x'],
#         cut_map_size['y'],
#         cut_map_size['x'] + cut_map_size['w'],
#         cut_map_size['y'] + cut_map_size['h']
#     ))
#     return cut_image
