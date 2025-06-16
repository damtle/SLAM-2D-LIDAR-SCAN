import json
from collections import OrderedDict


def load_json(input_file):
    """读取 JSON 文件"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data


def deduplicate_latest_pose(data, pose_tolerance=1e-6):
    """去重 JSON 数据，保留每个位姿的最新观测值"""
    map_data = data.get('map', {})
    if not map_data:
        print("No 'map' key found in JSON data")
        return data

    # 按时间戳排序
    sorted_entries = sorted(map_data.items(), key=lambda x: float(x[0]))

    # 存储每个位姿的最新记录
    pose_to_latest = OrderedDict()  # 使用 OrderedDict 保持插入顺序

    # 一次循环，按时间戳顺序处理
    for ts, entry in sorted_entries:
        pose = (entry['x'], entry['y'], entry['theta'])
        # 更新位姿的最新记录
        pose_to_latest[pose] = (ts, entry)

    # 构建去重后的 map 数据
    deduped_map = {}
    for ts, entry in pose_to_latest.values():
        deduped_map[ts] = entry

    # 更新 JSON 数据
    data['map'] = deduped_map
    return data


def save_json(data, output_file):
    """保存 JSON 数据"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    print(f"Saved deduplicated data to {output_file}")


def main(input_file='aces_gfs', output_file='aces_gfs_cleaned'):
    # 加载 JSON 数据
    data = load_json(input_file)

    # 去重，保留每个位姿的最新记录
    deduped_data = deduplicate_latest_pose(data, pose_tolerance=1e-6)

    # 保存结果
    save_json(deduped_data, output_file)


if __name__ == '__main__':
    main()