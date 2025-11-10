import os
import json

json_path = "/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_1/single_query_critique.json"
jsonl_path = json_path + "l"
with open(json_path, 'r') as f:
    json_list = json.load(f)

assert isinstance(json_list, list), "error: only for list(dict)"
assert isinstance(json_list[0], dict), "error: only for list(dict)"

with open(jsonl_path, "w") as f:
    for dict_item in json_list:
        f.write(json.dumps(dict_item) + '\n')