## 配置说明
### 当前功能说明
`map_utils`

```python
from algorithms import MapHelper
from PIL import Image


config_dict = {
    # ...
}
image = Image.open(image_path)
curren_map = 'buwanjia'
map_helper = MapHelper(
    map_config=config_dict,
)
map_helper.set_map_name(curren_map)
start_pos = map_helper.get_start_pos(image)
actual_path = map_helper.get_full_path()
_, direction = map_helper.find_next_coordinate_and_direction(actual_path, start_pos)
node = map_helper.get_map_info()['grid'][start_pos[0]][start_pos[1]]
door_pos = tuple(node.door_pos[direction])

print(f"当前坐标为:{start_pos} \n"
          f"当前坐标到终点的坐标集合为:{actual_path} \n"
          f"下一个门坐标:{door_pos} \n")
```

### `config` 字典结构

以下是 `map_utils` 类所需的 `map_config` 字典的结构：

- `map`: 描述用途的值（默认为 `'default_value'`）
- `buwanjia`: 副本的名称
- `buwanjia` `mid`: 副本途中必须经过的位置
- `buwanjia` `end`: 副本BOSS的位置
- `buwanjia` `grid`: 副本的矩阵比如布万加是3x6的
- `buwanjia` `grid` `x`: 矩阵的x坐标
- `buwanjia` `grid` `y`: 矩阵的y坐标
- `buwanjia` `grid` `unedges`: 矩阵中每个格子不可连接的方向
- `buwanjia` `grid` `connections`: 矩阵中每个格子可连接方向的相对位置的门坐标,通过站在门入口处获取

### 示例配置

```python
map_config = {
    'map': {
        "map_grid_size": [40,40] #这是每个格子相对于游戏分辨率的尺寸
        "buwanjia":{
            "mid": [1,1],
            "end": [1,5],
            "cut_map_size": {
                "x": 284,
                "y": 136,
                "w": 224,
                "h": 110
            },
        },
         "grid": [
            [
                {
                    "x": 0,
                    "y": 0,
                    "unedges": [
                        "top",
                        "left"
                    ],
                    "connections": {
                        "down": [
                            320,
                            371
                        ],
                        "right": [
                            636,
                            257
                        ]
                    }
                }
            ]
        ]
    }
}
```