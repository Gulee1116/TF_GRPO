# import os
# import re
# import json
# from pathlib import Path
# from typing import Iterator, List, Dict, Union, Optional
# import hashlib
# from collections import defaultdict

# def _findinfo(log_path:str):
#     """
#     从形如 'AIME24_pass_1_exp_y_20251106_042247_eval.txt' 的字符串中提取：
#     - dataset(如 AIME24)
#     - pass_id(如 pass_1)
#     - exp_id(如 exp_y)
#     - timestamp(如 20251106_042247)
#     """
#     pattern = re.compile(
#         r'^(?P<dataset>[A-Za-z0-9]+)_(?P<pass>pass_\d+)_exp_(?P<exp>[a-z]+)_(?P<time>\d{8}_\d{6})'
#     )

#     match = pattern.search(log_path)
#     if not match:
#         raise ValueError(f"文件名格式不符合预期: {log_path}")

#     return match.groupdict()

# def _findevallog(exp_name:str):
#     """
#     从/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/eval目录提取对应的完整log jsonline，可以用于计算在每道题上的表现
#     jsonline中的json format:
#     {
#         "runid": int,
#         "prompt": str,
#         "problem": str,
#         "groundtruth": str,
#         "retry_count": int,
#         "response": str,
#         "trajectories": list[dict],
#         "error": str or None,
#         "rollout_time": float,
#         "reward": float
#     }
#     """
#     exp_name = exp_name.split('.')[0]
#     EVAL_DIR = "/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/eval"
#     jsonl_path = os.path.join(EVAL_DIR, f'{exp_name}.jsonl')
#     results = []
#     with open(jsonl_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             try:
#                 data = json.loads(line)
#                 problem = data.get("problem")
#                 reward = data.get("reward")
#                 if problem is not None and reward is not None:
#                     results.append({
#                         "problem_hash": hashlib.md5(problem.encode("utf-8")).hexdigest(),
#                         "problem": problem[:50],
#                         "reward": reward
#                     })
#             except json.JSONDecodeError:
#                 # 跳过坏行
#                 continue
#     return results


# def _parse_metrics(filepath: str):
#     """
#     从形如:
#         - avg_reward: 0.7333333333333333
#         - Pass@1: 0.7333333333333333
#         - avg_tool_call: 2.6333333333333333
#     的txt文件中提取指标并返回字典。
#     """
#     metrics = {}
#     with open(filepath, 'r', encoding='utf-8') as f:
#         for line in f:
#             line = line.strip()
#             if not line or ':' not in line:
#                 continue
#             # 去掉前导的 '- ' 和空格
#             line = line.lstrip('-').strip()
#             key, value = [x.strip() for x in line.split(':', 1)]
#             try:
#                 value = float(value)
#             except ValueError:
#                 pass  # 保留原始字符串
#             metrics[key] = value
#     return metrics

# def scan_single_passk_res(passk_dir: str):
#     log_file_pathes = []
#     infoes = []
#     pass_k_processing = ""
#     for log_file_path in os.listdir(eval_results_dir):
#         # e.g. 'AIME24_pass_1_exp_y_20251106_042247_eval.txt'
#         if log_file_path.endswith(".txt"):
#             log_file_pathes.append(log_file_path)
            
#             info = _findinfo(log_file_path)
#             info['log_file_path'] = log_file_path
#             info |= _parse_metrics(os.path.join(eval_results_dir, log_file_path))
#             info['val_log'] = _findevallog(log_file_path)
            
#             pass_k = info['pass']
#             if not pass_k_processing: pass_k_processing = pass_k 
#             else: assert pass_k_processing == pass_k, "Error: this func is designed for processing single passk!"            
#             infoes.append(info)
            
#         elif log_file_path.endswith(".log"):pass
#         else: raise("something unknown exists in log file dir!")        
    
#     return infoes, pass_k

# eval_results_dir = "/home/wangziyue-20251013/TF_GRPO_local/training_free_grpo/eval_results/Qwen3-32B/pass1"
# pass_1_infoes, _ = scan_single_passk_res(eval_results_dir)

# data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
# for pass_i_info in pass_1_infoes:
#     dataset = pass_i_info['dataset']
#     exp = pass_i_info['exp']
#     for val_log in pass_i_info['val_log']:
#         data[dataset][exp][val_log['problem']].append(val_log['reward'])    
# data = dict(data)

# def AIME_PASS_k(data, k):

#     print("\n\nAIME24")
#     AIME24_y_passk = 0
#     for sample in data['AIME24']['y'].values():
#         if sum(sample[:k]) > 0:
#             AIME24_y_passk +=1 / len(data['AIME24']['y'].values())

#     print(f"AIME24_y_pass{k}:{AIME24_y_passk}")

#     AIME24_n_passk = 0
#     for sample in data['AIME24']['n'].values():
#         if sum(sample[:k]) > 0:
#             AIME24_n_passk +=1 / len(data['AIME24']['n'].values())
#     print(f"AIME24_n_pass{k}:{AIME24_n_passk}")

#     print("\n\nAIME25")
#     AIME25_y_passk = 0
#     for sample in data['AIME25']['y'].values():
#         if sum(sample[:k]) > 0:
#             AIME25_y_passk +=1 / len(data['AIME25']['y'].values())

#     print(f"AIME25_y_pass{k}:{AIME25_y_passk}")

#     AIME25_n_passk = 0
#     for sample in data['AIME25']['n'].values():
#         if sum(sample[:k]) > 0:
#             AIME25_n_passk +=1 / len(data['AIME25']['n'].values())
#     print(f"AIME25_n_pass{k}:{AIME25_n_passk}")

# AIME_PASS_k(data, 8)




import os
import re
import json
from typing import Dict, List
import hashlib
from collections import defaultdict

def _findinfo(log_path:str):
    """
    从形如 'AIME24_pass_1_exp_y_20251106_042247_eval.txt' 的字符串中提取：
    - dataset(如 AIME24)
    - pass(如 pass_1)
    - exp(如 y)
    - time(如 20251106_042247)
    """
    pattern = re.compile(
        r'^(?P<dataset>[A-Za-z0-9]+)_(?P<pass>pass_\d+)_exp_(?P<exp>[a-z]+)_(?P<time>\d{8}_\d{6})'
    )
    match = pattern.search(log_path)
    if not match:
        raise ValueError(f"文件名格式不符合预期: {log_path}")
    return match.groupdict()

def _safe_count_tool_calls(x):
    """
    尽量健壮地统计单条记录里的 tool call 次数：
      - list: 长度
      - dict: 视为 1（或看其中的 'calls' 列表长度）
      - int/float: 直接取整
      - 其他/None: 0
    """
    if x is None:
        return 0
    if isinstance(x, list):
        return len(x)
    if isinstance(x, dict):
        # 常见结构兜底：{'calls': [ ... ]}
        if 'calls' in x and isinstance(x['calls'], list):
            return len(x['calls'])
        return 1
    if isinstance(x, (int, float)):
        return int(x)
    return 0

def _findevallog(exp_name:str):
    """
    读取对应的 .jsonl，提取每条尝试：
      返回列表，每项包含：
        - problem_hash: str
        - reward: float
        - tool_calls: int
        - runid: int (用于排序)
    """
    exp_name = exp_name.split('.')[0]
    EVAL_DIR = "/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/eval"
    jsonl_path = os.path.join(EVAL_DIR, f'{exp_name}.jsonl')
    results = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                problem = data.get("problem")
                if problem is None:
                    continue
                reward = data.get("reward")
                # reward 兜底：无法转成 float 则跳过该行
                try:
                    reward = float(reward)
                except (TypeError, ValueError):
                    continue

                runid = data.get("runid")
                # 没有 runid 也尽量兜底为 0（不过强烈建议生成侧保证 runid）
                try:
                    runid = int(runid)
                except (TypeError, ValueError):
                    runid = 0

                tc = _safe_count_tool_calls(data.get("tool_calls"))

                results.append({
                    "problem_hash": hashlib.md5(problem.encode("utf-8")).hexdigest(),
                    "reward": reward,
                    "tool_calls": tc,
                    "runid": runid,
                })
            except json.JSONDecodeError:
                # 跳过坏行
                continue
    return results

def _parse_metrics(filepath: str):
    """
    从形如:
        - avg_reward: 0.7333333333333333
        - Pass@1: 0.7333333333333333
        - avg_tool_call: 2.6333333333333333
    的txt文件中提取指标并返回字典。
    """
    metrics = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            line = line.lstrip('-').strip()
            key, value = [x.strip() for x in line.split(':', 1)]
            try:
                value = float(value)
            except ValueError:
                pass
            metrics[key] = value
    return metrics

def scan_single_passk_res(passk_dir: str):
    """
    只处理一个 pass_k 目录，返回：
      - infoes: 每个 txt 的解析信息（含 metrics 与对应 jsonl 的明细）
      - pass_k: 当前处理的 pass_k（如 'pass_1'）
    """
    infoes = []
    pass_k_processing = ""
    for log_file_path in os.listdir(passk_dir):
        # e.g. 'AIME24_pass_1_exp_y_20251106_042247_eval.txt'
        if log_file_path.endswith(".txt"):
            info = _findinfo(log_file_path)
            info['log_file_path'] = log_file_path
            info |= _parse_metrics(os.path.join(passk_dir, log_file_path))
            info['val_log'] = _findevallog(log_file_path)

            pass_k = info['pass']
            if not pass_k_processing:
                pass_k_processing = pass_k
            else:
                assert pass_k_processing == pass_k, "Error: this func is designed for processing single passk!"
            infoes.append(info)

        elif log_file_path.endswith(".log"):
            continue
        else:
            raise RuntimeError("something unknown exists in log file dir!")
    return infoes, pass_k_processing

# ===== 使用上面的扫描函数 =====
eval_results_dir = "/home/wangziyue-20251013/TF_GRPO_local/training_free_grpo/eval_results/Qwen3-32B/pass1"
pass_1_infoes, _ = scan_single_passk_res(eval_results_dir)

# ===== 按 dataset/exp/problem_hash 聚合（并按 runid 排序）=====
# data[dataset][exp][problem_hash] = {
#     "rewards": [ ... ],
#     "tool_calls": [ ... ]
# }
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"rewards": [], "tool_calls": []})))
# 额外：为“全局平均 tool calls（按记录）”做计数
global_tool_calls_by_group = defaultdict(lambda: defaultdict(list))  # [dataset][exp] -> [counts...]

for pass_i_info in pass_1_infoes:
    dataset = pass_i_info['dataset']
    exp = pass_i_info['exp']  # 'y' 或 'n'
    # 先按 problem_hash 分桶收集，再按 runid 排序
    bucket = defaultdict(list)  # problem_hash -> list of dicts
    for row in pass_i_info['val_log']:
        bucket[row["problem_hash"]].append(row)
        global_tool_calls_by_group[dataset][exp].append(row["tool_calls"])
    # 排序写回
    for phash, rows in bucket.items():
        rows_sorted = sorted(rows, key=lambda x: x["runid"])
        data[dataset][exp][phash]["rewards"].extend([r["reward"] for r in rows_sorted])
        data[dataset][exp][phash]["tool_calls"].extend([r["tool_calls"] for r in rows_sorted])

data = {ds: dict(exps) for ds, exps in data.items()}

def _compute_metrics_at_k(samples_by_problem: Dict[str, Dict[str, List[float]]], k: int):
    """
    输入:
      samples_by_problem: {problem_hash: {"rewards": [...], "tool_calls": [...]}}
    返回:
      pass_at_k: float
      mean_reward_at_k: float
      mean_tool_calls_at_k: float
    规则:
      - 仅使用每题的前 k 次（若不足 k 次则用实际次数）
      - pass@k: 前 k 次里是否有 reward>0
      - mean_reward@k: 每题前 k 次 reward 的平均，再对题平均
      - mean_tool_calls@k: 每题前 k 次 tool_calls 的平均，再对题平均
    """
    if not samples_by_problem:
        return 0.0, 0.0, 0.0

    n = len(samples_by_problem)
    pass_cnt = 0
    reward_mean_sum = 0.0
    tool_mean_sum = 0.0

    for rec in samples_by_problem.values():
        rw = rec["rewards"][:k]
        tc = rec["tool_calls"][:k]
        # pass@k
        if any(r > 0 for r in rw):
            pass_cnt += 1
        # mean@k（不足 k 次按已有次数平均）
        denom_r = max(1, len(rw))
        denom_t = max(1, len(tc))
        reward_mean_sum += sum(rw) / denom_r
        tool_mean_sum += sum(tc) / denom_t

    pass_at_k = pass_cnt / n
    mean_reward_at_k = reward_mean_sum / n
    mean_tool_calls_at_k = tool_mean_sum / n
    return pass_at_k, mean_reward_at_k, mean_tool_calls_at_k

def _global_avg_tool_calls(counts: List[int]) -> float:
    if not counts:
        return 0.0
    return sum(counts) / len(counts)

def AIME_METRICS_k(data, k):
    """
    同时打印 AIME24/AIME25 下 exp=y/n 的：
      - pass@k
      - mean_reward@k
      - mean_tool_calls@k
      - global_avg_tool_calls（跨所有记录的平均，不按题聚合）
    """
    for ds in ["AIME24", "AIME25"]:
        print(f"\n\n{ds}")
        for exp in ["y", "n"]:
            samples = data.get(ds, {}).get(exp, {})
            p_at_k, m_reward_k, m_tool_k = _compute_metrics_at_k(samples, k)
            print(f"{ds}_{exp}_pass@{k}: {p_at_k}")
            print(f"{ds}_{exp}_mean_reward@{k}: {m_reward_k}")
            print(f"{ds}_{exp}_mean_tool_calls@{k}: {m_tool_k}")

            g_counts = global_tool_calls_by_group.get(ds, {}).get(exp, [])
            print(f"{ds}_{exp}_global_avg_tool_calls: {_global_avg_tool_calls(g_counts)}")

# 运行
AIME_METRICS_k(data, 8)
