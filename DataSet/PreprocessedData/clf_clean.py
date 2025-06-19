import json

# Step 1: 读取 relations 数据，提取所有需要的时间戳
with open("intel_relation_processed", "r") as f:
    relations = json.load(f)
    ts1_keys = set(map(float, relations['relation_timeStamp1'].keys()))
    ts2_keys = set(map(float, relations['relation_timeStamp2'].keys()))
    all_needed_timestamps = ts1_keys.union(ts2_keys)

# Step 2: 读取原始 clf 数据
with open("intel_clf", "r") as f:
    clf_data = json.load(f)['map']

# Step 3: 精简数据，只保留需要的时间戳对应的激光帧
filtered_clf = {
    str(t): data
    for t, data in clf_data.items()
    if float(t) in all_needed_timestamps
}

# Step 4: 写出精简后的文件
with open("intel_clf_filtered.json", "w") as f:
    json.dump({'map': filtered_clf}, f, indent=4, sort_keys=True)
