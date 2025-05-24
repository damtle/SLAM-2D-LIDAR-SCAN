import json
import math
import numpy as np

# Load the JSON data
with open('../DataSet/PreprocessedData/fr079_gfs', 'r') as file:
    data = json.load(file)

# 初始化地图边界变量
min_x, max_x = float('inf'), float('-inf')
min_y, max_y = float('inf'), float('-inf')

# 处理每个扫描数据
for timestamp, scan in data['map'].items():
    x = scan['x']
    y = scan['y']
    theta = scan['theta']
    ranges = scan['range']

    # 假设360°视野，距离值均匀分布
    num_ranges = len(ranges)
    angle_increment = 2 * math.pi / num_ranges  # 相邻测量点的角度增量
    angles = np.arange(-math.pi, math.pi, angle_increment)[:num_ranges]

    # 计算每个距离值的终点坐标
    for r, angle in zip(ranges, angles):
        if r >= 81.83:  # 跳过无效或最大距离值
            continue
        # 计算激光束的全局角度
        global_angle = theta + angle
        # 计算终点坐标
        x_end = x + r * math.cos(global_angle)
        y_end = y + r * math.sin(global_angle)
        # 更新边界
        min_x = min(min_x, x_end)
        max_x = max(max_x, x_end)
        min_y = min(min_y, y_end)
        max_y = max(max_y, y_end)

# 计算地图大小
width = max_x - min_x
height = max_y - min_y

# 打印结果
print("地图边界：")
print(f"  X: [{min_x:.2f}, {max_x:.2f}]")
print(f"  Y: [{min_y:.2f}, {max_y:.2f}]")
print("地图大小：")
print(f"  宽度: {width:.2f} 米")
print(f"  高度: {height:.2f} 米")