import cv2
import numpy as np

# 定义蓝色的 HSV 范围（根据实际图片调整）
BLUE_HSV_LOWER = np.array([95, 152, 45])
BLUE_HSV_UPPER = np.array([110, 255, 255])


def find_blue_object_and_grid(image, grid_size=(100, 100), display=False):
    """
    在图像中找到蓝色对象，并在图像上绘制网格。

    参数:
    - image: 输入图像（可以是灰度图或彩色图）
    - grid_size: 网格的大小（宽度和高度）
    - display: 是否显示结果图像

    返回:
    - grid_img: 带网格和蓝色对象标记的图像
    - grid_coordinates: 蓝色对象所在的网格坐标（如果找到蓝色对象），否则为 None
    """

    # 确保输入图像是 NumPy 数组
    image = np.array(image)
    # 如果输入是灰度图像，将其转换为 BGR 彩色图像
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 转换到 HSV 色彩空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 创建掩模，提取蓝色区域
    blue_mask = cv2.inRange(hsv_image, BLUE_HSV_LOWER, BLUE_HSV_UPPER)

    # 查找掩模中的轮廓
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 选择最大的轮廓
        largest_contour = max(contours, key=cv2.contourArea)

        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(largest_contour)

        # 绘制蓝色对象的边界框
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 计算蓝色对象的中心点
        center_x, center_y = x + w // 2, y + h // 2

        # 创建网格图像副本
        grid_img = image.copy()
        img_height, img_width = grid_img.shape[:2]

        # 绘制网格
        for i in range(0, img_width, grid_size[0]):
            for j in range(0, img_height, grid_size[1]):
                cv2.rectangle(grid_img, (i, j), (i + grid_size[0], j + grid_size[1]), (255, 0, 0), 1)

        # 计算网格坐标
        grid_x = center_x // grid_size[0]
        grid_y = center_y // grid_size[1]

        # 在图像上标记网格坐标
        grid_coords_text = f"({grid_y}, {grid_x})"
        text_position = (center_x, max(center_y - 10, 0))
        cv2.putText(grid_img, grid_coords_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 显示结果图像
        if display:
            from algorithms.visualization.gui import show_cv_gui_one
            show_cv_gui_one(grid_img, (grid_y, grid_x))

        return grid_img, (grid_y, grid_x)

    print("No blue object found.")
    return image, None

