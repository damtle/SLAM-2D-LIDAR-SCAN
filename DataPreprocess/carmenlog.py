import json


def parse_carmen_log(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[0] == 'FLASER':
                timestamp = float(parts[-3])
                range_data = list(map(float, parts[2:-9]))
                pos = parts[-6:-3]
                data[timestamp] = {
                    'range': range_data,
                    "theta": float(pos[0]),
                    "x": float(pos[1]),
                    "y": float(pos[2])
                }
    return data


def convert_to_gfs(data):
    gfs_data = {}
    for timestamp in sorted(data.keys()):
        entry = data[timestamp]
        if 'range' in entry:
            gfs_data[str(timestamp)] = {
                'range': entry['range'],
                'x': entry['x'],
                'y': entry['y'],
                'theta': entry['theta']
            }
    return gfs_data


def save_gfs_file(gfs_data, output_file):
    with open(output_file, 'w') as file:
        json.dump({'map': gfs_data}, file, indent=4)


# 主函数
if __name__ == '__main__':
    carmen_log_file = "../DataSet/RawData/fr079.clf"
    output_gfs_file = "../DataSet/PreprocessedData/fr079_gfs"

    # 解析 CARMEN 日志文件
    parsed_data = parse_carmen_log(carmen_log_file)

    # 转换为 GFS 格式
    gfs_data = convert_to_gfs(parsed_data)

    # 保存为 GFS 文件
    save_gfs_file(gfs_data, output_gfs_file)
    print(f"GFS 文件已保存到 {output_gfs_file}")