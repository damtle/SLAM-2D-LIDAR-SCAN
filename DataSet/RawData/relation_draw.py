import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def read_relations(relations_file):
    """读取 .relations 文件，返回时间戳对和相对位姿"""
    relations = []
    with open(relations_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) != 8:
                continue
            t1, t2 = float(parts[0]), float(parts[1])
            x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
            roll, pitch, yaw = float(parts[5]), float(parts[6]), float(parts[7])
            relations.append((t1, t2, x, y, z, roll, pitch, yaw))
    return relations


def compute_absolute_trajectory(relations):
    """根据相对位姿计算绝对位姿轨迹"""
    # 初始位姿 (x, y, theta)
    x, y, theta = 0.0, 0.0, 0.0
    trajectory = [(0.0, x, y, theta)]  # (timestamp, x, y, theta)

    # 按时间戳顺序处理
    for t1, t2, dx, dy, dz, droll, dpitch, dyaw in sorted(relations, key=lambda r: r[0]):
        # 旋转矩阵转换相对位移到世界坐标系
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        world_dx = dx * cos_theta - dy * sin_theta
        world_dy = dx * sin_theta + dy * cos_theta
        # 更新绝对位姿
        x += world_dx
        y += world_dy
        theta += dyaw
        trajectory.append((t2, x, y, theta))

    return trajectory


def plot_trajectory(trajectory, output_file='trajectory.png'):
    """绘制轨迹并保存为 PNG"""
    timestamps = [t for t, x, y, theta in trajectory]
    x_coords = [x for t, x, y, theta in trajectory]
    y_coords = [y for t, x, y, theta in trajectory]

    # 计算绘图范围
    buffer = 1.0  # 米，增加边界缓冲
    x_min, x_max = min(x_coords) - buffer, max(x_coords) + buffer
    y_min, y_max = min(y_coords) - buffer, max(y_coords) + buffer
    # 确保最小范围
    min_span = 10.0
    if x_max - x_min < min_span:
        x_min, x_max = x_min - min_span / 2, x_min + min_span / 2
    if y_max - y_min < min_span:
        y_min, y_max = y_min - min_span / 2, y_min + min_span / 2

    plt.figure(figsize=(19.20, 19.20))
    colors = iter(cm.rainbow(np.linspace(1, 0, len(x_coords))))
    for i in range(len(x_coords)):
        plt.scatter(x_coords[i], y_coords[i], color=next(colors), s=35)
    plt.scatter(x_coords[0], y_coords[0], color='r', s=500, label='Start')
    plt.scatter(x_coords[-1], y_coords[-1], color='b', s=500, label='End')
    plt.plot(x_coords, y_coords, 'k-', label='Trajectory')

    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Robot Trajectory from Relations')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # 保持 x, y 比例一致
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.savefig(output_file)
    plt.close()


def main():
    relations_file = "intel.relations"  # 替换为您文件的实际路径
    relations = read_relations(relations_file)
    trajectory = compute_absolute_trajectory(relations)
    plot_trajectory(trajectory, 'trajectory.png')


if __name__ == '__main__':
    main()