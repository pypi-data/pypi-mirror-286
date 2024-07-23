import heapq
from algorithms.pathfinding.grid_node import get_neighbors, reconstruct_path


def heuristic(a, b):
    """
    计算两点之间的曼哈顿距离作为启发式函数。

    参数:
    - a: 起始点 (GridNode)
    - b: 目标点 (GridNode)

    返回:
    - 曼哈顿距离 (int)
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar(grid, start_pos, end_pos):
    """
    A* 算法用于在网格中寻找从起点到终点的最短路径。

    参数:
    - grid: 网格（二维列表，包含 GridNode 对象）
    - start_pos: 起点坐标（列表或元组，包含两个整数）
    - end_pos: 终点坐标（列表或元组，包含两个整数）

    返回:
    - 最短路径的节点列表，如果没有路径则返回 None
    """
    # 验证 start_pos 和 end_pos 的有效性
    for pos in [start_pos, end_pos]:
        if not isinstance(pos, (list, tuple)) or len(pos) != 2:
            raise ValueError(f"{pos} 必须是一个包含两个整数的列表或元组")
        if not (isinstance(pos[0], int) and isinstance(pos[1], int)):
            raise ValueError(f"{pos} 必须包含两个整数")
        if not (0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])):
            raise ValueError(f"{pos} 超出网格边界")

    start_node = grid[start_pos[0]][start_pos[1]]
    goal_node = grid[end_pos[0]][end_pos[1]]

    # 初始化起点
    start_node.g_cost = 0
    start_node.h_cost = heuristic(start_node, goal_node)
    start_node.f_cost = start_node.g_cost + start_node.h_cost

    # 优先级队列
    open_list = []
    heapq.heappush(open_list, (start_node.f_cost, start_node))

    # 已访问节点集合
    closed_list = {}

    while open_list:
        _, current = heapq.heappop(open_list)

        # 如果到达目标节点，返回路径
        if (current.x, current.y) == (goal_node.x, goal_node.y):
            return reconstruct_path(current)

        closed_list[(current.x, current.y)] = current

        # 遍历邻居节点
        for neighbor in get_neighbors(current, grid):
            if (neighbor.x, neighbor.y) in closed_list:
                continue

            tentative_g_cost = current.g_cost + 1

            if neighbor not in [node for _, node in open_list] or tentative_g_cost < neighbor.g_cost:
                neighbor.parent = current
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = heuristic(neighbor, goal_node)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost

                if neighbor not in [node for _, node in open_list]:
                    heapq.heappush(open_list, (neighbor.f_cost, neighbor))

    # 如果没有路径，返回 None
    return None
