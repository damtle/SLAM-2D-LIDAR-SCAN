import json
import numpy as np


def parse_carmen_log(input_file):
    flaser_data = []
    odom_data = []

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'FLASER':
                # FLASER format: FLASER num_readings [range_readings] x y theta odom_x odom_y odom_theta timestamp hostname logger_timestamp
                num_readings = int(parts[1])
                ranges = [float(r) for r in parts[2:2 + num_readings]]
                timestamp = float(
                    parts[2 + num_readings + 6])  # timestamp is after x, y, theta, odom_x, odom_y, odom_theta
                flaser_data.append({
                    'timestamp': timestamp,
                    'ranges': ranges
                })

            elif parts[0] == 'ODOM':
                # ODOM format: ODOM x y theta tv rv accel timestamp hostname logger_timestamp
                x = float(parts[1])
                y = float(parts[2])
                theta = float(parts[3])
                timestamp = float(parts[7])
                odom_data.append({
                    'timestamp': timestamp,
                    'x': x,
                    'y': y,
                    'theta': theta
                })

    return flaser_data, odom_data


def find_closest_odom(flaser_timestamp, odom_data):
    # Find the ODOM record with the closest timestamp
    closest_odom = min(odom_data, key=lambda odom: abs(odom['timestamp'] - flaser_timestamp))
    return closest_odom


def convert_to_json(flaser_data, odom_data):
    json_output = {}

    for flaser in flaser_data:
        timestamp = flaser['timestamp']
        closest_odom = find_closest_odom(timestamp, odom_data)

        json_output[str(timestamp)] = {
            'range': flaser['ranges'],
            'x': closest_odom['x'],
            'y': closest_odom['y'],
            'theta': closest_odom['theta']
        }

    return json_output


def main(input_file='fr079.clf', output_file='fr079_gfs'):
    # Parse the input file
    flaser_data, odom_data = parse_carmen_log(input_file)

    # Convert to JSON format
    json_data = convert_to_json(flaser_data, odom_data)

    wrapped_data = {
        "maps": json_data,
    }

    # Write to output file
    with open(output_file, 'w') as f:
        json.dump(wrapped_data, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()