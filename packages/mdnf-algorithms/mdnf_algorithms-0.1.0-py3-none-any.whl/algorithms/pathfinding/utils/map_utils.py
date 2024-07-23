from typing import Any, Dict, Tuple, List
from algorithms.image_processing.cut_map import cut_map_grid
from algorithms.image_processing.find_blue_object import find_blue_object_and_grid
from algorithms.pathfinding.grid_node import create_grid_nodes
from algorithms.pathfinding.astar import astar



class MapHelper:
    def __init__(self,
                 map_config: Dict,
                 ):

        self.config = map_config
        self.map_config = self.config.get('map')
        self.map_name = ""
        self.start_pos = (-1, -1)  # 初始为 (-1, -1) 表示未设置
        self.map_grid_size = self.map_config['map_grid_size']

        self.cut_map_fn = cut_map_grid
        self.find_object_fn = find_blue_object_and_grid
        self.create_grid_nodes_fn = create_grid_nodes
        self.astar_fn = astar

    def set_map_name(self, map_name: str):
        self.map_name = map_name

    def get_map_info(self) -> Dict[str, Any]:
        if not isinstance(self.map_config, dict) or self.map_name not in self.map_config:
            raise ValueError(f"No map found with the name '{self.map_name}'")

        current_map = self.map_config[self.map_name]
        return {
            'mid': tuple(current_map['mid']),
            'end': tuple(current_map['end']),
            'grid': self.create_grid_nodes_fn(current_map.get('grid', []))
        }

    def get_start_pos(self, image: Any) -> Tuple[int, int]:
        if self.map_name == "":
            print("未设置当前地图")
            return -1, -1

        cut_map_size = self.map_config[self.map_name]['cut_map_size']
        map_grid_size = self.get_map_grid_size()
        map_image = self.cut_map_fn(image, cut_map_size)
        _, start_pos = self.find_object_fn(map_image, map_grid_size)

        print(f"Start position found: {start_pos}")

        self.start_pos = start_pos
        print(f"Start position set to: {start_pos}")
        return start_pos

    def get_map_grid_size(self) -> Tuple[int, int]:
        if self.map_grid_size != (-1, -1):
            return self.map_grid_size
        return self.map_config.get('map_grid_size', (-1, -1))

    def get_short_path(self, grid: List[List[Any]], start_pos: Tuple[int, int] = None,
                       end_pos: Tuple[int, int] = None) -> List[Tuple[int, int]]:
        if not all(isinstance(row, list) for row in grid):
            raise ValueError("The grid must be a 2D list of GridNode objects")

        self.reset_node_states(grid)
        start_pos = start_pos or self.start_pos
        if self.start_pos == (-1, -1):
            print("未获取起始坐标")
        return self.astar_fn(grid, start_pos, end_pos)

    def get_full_path(self, show: bool = False) -> List[Tuple[int, int]]:
        map_info = self.get_map_info()

        if map_info['end'] == (0, 0) or not map_info['grid']:
            print('没有记录当前地图')
            return []

        grid = map_info['grid']
        mid_path = self.get_short_path(grid, end_pos=map_info.get('mid')) if 'mid' in map_info else []

        if mid_path:
            end_path = self.get_short_path(grid, start_pos=map_info['mid'], end_pos=map_info['end']) or []
            end_pos = mid_path + end_path
        else:
            end_pos = self.get_short_path(grid, end_pos=map_info['end'])

        if show and self.show_fn:
            from algorithms.visualization.gui import show_plt_gui
            show_plt_gui(end_pos, grid)

        return end_pos

    @staticmethod
    def reset_node_states(grid: List[List[Any]]):
        for row in grid:
            for node in row:
                node.g_cost = float('inf')
                node.h_cost = 0
                node.f_cost = float('inf')
                node.parent = None

    @staticmethod
    def find_next_coordinate_and_direction(path: List[Tuple[int, int]], start: Tuple[int, int]) -> Tuple[
        Tuple[int, int], str]:
        if start not in path:
            return None, None

        start_index = path.index(start)

        for next_coordinate in path[start_index + 1:]:
            if next_coordinate != start:
                dx = next_coordinate[1] - start[1]
                dy = next_coordinate[0] - start[0]

                if dx > 0:
                    direction = "right"
                elif dx < 0:
                    direction = "left"
                elif dy > 0:
                    direction = "down"
                else:
                    direction = "top"

                return next_coordinate, direction

        return None, None

    def reset_map_state(self):
        self.map_config = self.config.get_config('map')
        self.map_name = ""
        self.start_pos = (-1, -1)
