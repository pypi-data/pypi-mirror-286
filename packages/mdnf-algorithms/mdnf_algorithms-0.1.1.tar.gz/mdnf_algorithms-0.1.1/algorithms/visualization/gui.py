import matplotlib.pyplot as plt
import numpy as np
import cv2


def show_plt_gui(path, grid):
    if path:
        # 将 grid 转换为 NumPy 数组，以便高效操作
        visual_grid = np.zeros((len(grid), len(grid[0])), dtype=np.uint8)

        # 将路径上的点标记为 2（或其他可区分的值）
        for i, (x, y) in enumerate(path):
            visual_grid[x, y] = 2 if i != len(path) - 1 else 3  # 终点用 3 表示

        # 可视化网格
        plt.figure(figsize=(8, 8))
        plt.imshow(visual_grid, cmap='hot', interpolation='nearest')
        plt.colorbar(label='Value')
        plt.title('Grid Visualization with Path')
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.show()
    else:
        print("No path provided.")


def show_cv_gui(img, grid_coords):
    if img is not None:
        # 如果有 grid_coords，绘制网格（例如：绿色）
        if grid_coords:
            print(grid_coords)
            for (x, y) in grid_coords:
                cv2.circle(img, (y, x), 5, (0, 255, 0), -1)  # 绘制绿色圆点

        cv2.imshow('Grid and Blue Object', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No image provided.")


def show_cv_gui_one(img, grid_coords):
    if grid_coords is not None:
        cv2.imshow('Grid and Blue Object', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No blue object found.")
