import re

def read_slam_log(slam_log_file):
    trajectory = {}
    with open(slam_log_file, 'r') as f:
        for line in f:
            if line.startswith('FLASER'):
                tokens = line.split()
                num_readings = int(tokens[1])
                x = float(tokens[num_readings + 2])
                y = float(tokens[num_readings + 3])
                theta = float(tokens[num_readings + 4])
                timestamp = float(tokens[num_readings + 8])
                trajectory[timestamp] = {'x': x, 'y': y, 'theta': theta}
    return trajectory

slam_trajectory = read_slam_log("slam.log")