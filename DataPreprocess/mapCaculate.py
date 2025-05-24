import numpy as np

# 从文件中读取数据
def read_data(file_path):
    x_positions = []
    y_positions = []
    max_lidar_range = 0
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'FLASER':
                num_readings = int(parts[1])
                range_data = list(map(float, parts[2:2 + num_readings]))
                max_lidar_range = max(max_lidar_range, max(range_data))
            elif parts[0] == 'ODOM':
                x = float(parts[1])
                y = float(parts[2])
                x_positions.append(x)
                y_positions.append(y)
    return x_positions, y_positions, max_lidar_range

# 计算地图大小
def calculate_map_size(x_positions, y_positions, max_lidar_range):
    min_x = min(x_positions)
    max_x = max(x_positions)
    min_y = min(y_positions)
    max_y = max(y_positions)
    map_width = (max_x - min_x) + 2 * max_lidar_range
    map_height = (max_y - min_y) + 2 * max_lidar_range
    return map_width, map_height

# 主函数
if __name__ == '__main__':
    file_path = '../DataSet/PreprocessedData/fr079_gfs'
    x_positions, y_positions, max_lidar_range = read_data(file_path)
    map_width, map_height = calculate_map_size(x_positions, y_positions, max_lidar_range)
    print(f"Estimated Map Size: Width = {map_width:.2f} meters, Height = {map_height:.2f} meters")