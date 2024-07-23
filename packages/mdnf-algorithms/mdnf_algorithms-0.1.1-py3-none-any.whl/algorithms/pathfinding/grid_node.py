class GridNode:
    def __init__(self, x, y, directions=None, door_pos=None):
        self.x = x
        self.y = y
        self.parent = None
        self.g_cost = float('inf')
        self.h_cost = 0
        self.f_cost = float('inf')
        self.door_pos = door_pos

        if directions is None or directions is []:

            # 默认所有方向都可移动  

            self.directions = ['left', 'right', 'top', 'down']

        else:

            self.directions = directions

    def __lt__(self, other):
        return self.f_cost < other.f_cost


def get_neighbors(node, grid):
    neighbors = []

    # 检查左方向  
    if 'None' in node.directions:

        # print(f"节点 {node} 没有邻居。")
        return neighbors

    else:
        if 'left' in node.directions:

            nx, ny = node.x - 1, node.y  # 向左移动  

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append(grid[nx][ny])

                # 检查右方向

        if 'right' in node.directions:

            nx, ny = node.x + 1, node.y  # 向右移动  

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append(grid[nx][ny])

                # 检查上方向

        if 'top' in node.directions:

            nx, ny = node.x, node.y - 1  # 向上移动  

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append(grid[nx][ny])

                # 检查下方向

        if 'down' in node.directions:

            nx, ny = node.x, node.y + 1  # 向下移动  

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append(grid[nx][ny])

        else:
            nx, ny = node.x, node.y

    return neighbors


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]


def create_grid_nodes(grid_data):
    nodes = []
    for grid_row in grid_data:
        sub_nodes = []
        for node_info in grid_row:
            x = node_info['x']
            y = node_info['y']
            directions = node_info.get('unedges', [])
            if directions == []:
                directions = None
            connections = node_info.get('connections', {})
            node_instance = GridNode(x, y, directions, connections)
            sub_nodes.append(node_instance)
        nodes.append(sub_nodes)
    return nodes
