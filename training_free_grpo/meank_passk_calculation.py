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
import hashlib
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# -------------------------------
# 解析文件名信息
# -------------------------------
def _findinfo(log_path: str) -> Dict[str, str]:
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

# -------------------------------
# 递归统计 tool_calls
# -------------------------------
def _parse_tool_calls_field(val: Any) -> int:
    """把可能是 list / str(内含JSON) / 其它 的 tool_calls 字段变成计数"""
    if isinstance(val, list):
        return len(val)
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
            return len(parsed) if isinstance(parsed, list) else 0
        except json.JSONDecodeError:
            return 0
    if isinstance(val, dict):
        # 某些结构可能是 {"calls": [...]} 或 {"data":[...]}；尽量兜底
        if "calls" in val and isinstance(val["calls"], list):
            return len(val["calls"])
        return 1  # 把 dict 当作一次 tool 调用集合
    if isinstance(val, (int, float)):
        return int(val)
    return 0

def _recursive_count_tool_calls(obj: Any) -> int:
    """
    递归地在任意层级统计 'tool_calls' 的数量。
    如果同一层里有多个 'tool_calls' 字段，会累加它们。
    """
    cnt = 0
    if isinstance(obj, dict):
        if "tool_calls" in obj:
            cnt += _parse_tool_calls_field(obj["tool_calls"])
        for v in obj.values():
            cnt += _recursive_count_tool_calls(v)
    elif isinstance(obj, list):
        for it in obj:
            cnt += _recursive_count_tool_calls(it)
    return cnt

# -------------------------------
# 解析 .jsonl 评测明细
# -------------------------------
def _findevallog(exp_name: str) -> List[Dict[str, Any]]:
    """
    读取 {exp_name}.jsonl，每行抽取：
      - problem_hash
      - reward
      - tool_calls (递归统计所有层级的 'tool_calls' 次数)
      - runid (若存在)
      - order (若 runid 缺失，则在每题内自增生成的顺序号，用于排序)
    """
    exp_name = exp_name.split('.')[0]
    EVAL_DIR = "/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/eval"
    jsonl_path = os.path.join(EVAL_DIR, f"{exp_name}.jsonl")

    results: List[Dict[str, Any]] = []
    # 对于缺 runid 的情况，按题目维度提供一个自增顺序
    per_problem_counter: Dict[str, int] = defaultdict(int)

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # 跳过坏行
                continue

            problem = data.get("problem")
            reward = data.get("reward")
            if problem is None or reward is None:
                continue

            problem_hash = hashlib.md5(problem.encode("utf-8")).hexdigest()

            # 递归统计这一行里所有层级出现的 tool_calls
            tool_calls_count = _recursive_count_tool_calls(data)

            runid = data.get("runid")
            # 若 runid 缺失，则为该题生成一个自增 order
            if runid is None:
                per_problem_counter[problem_hash] += 1
                order = per_problem_counter[problem_hash]
            else:
                order = None  # 有 runid 就不需要 order 参与排序

            results.append({
                "problem_hash": problem_hash,
                "reward": float(reward),
                "tool_calls": int(tool_calls_count),  # 统一字段名
                "runid": runid if runid is not None else None,
                "order": order,
            })

    return results

# -------------------------------
# 解析聚合指标文件
# -------------------------------
def _parse_metrics(filepath: str) -> Dict[str, float]:
    """
    从形如:
        - avg_reward: 0.7333333333333333
        - Pass@1: 0.7333333333333333
        - avg_tool_call: 2.6333333333333333
    的txt文件中提取指标并返回字典。
    """
    metrics: Dict[str, float] = {}
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

# -------------------------------
# 扫描单个 pass_k 目录
# -------------------------------
def scan_single_passk_res(passk_dir: str):
    """
    只处理一个 pass_k 目录，返回：
      - infoes: 每个 txt 的解析信息（含 metrics 与对应 jsonl 的明细）
      - pass_k: 当前处理的 pass_k（如 'pass_1'）
    """
    infoes: List[Dict[str, Any]] = []
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

# -------------------------------
# 构建数据结构
# -------------------------------
eval_results_dir = "/home/wangziyue-20251013/TF_GRPO_local/training_free_grpo/eval_results/Qwen3-32B/pass1"
pass_1_infoes, _ = scan_single_passk_res(eval_results_dir)

# data[dataset][exp][problem_hash] = {"rewards": [...], "tool_calls": [...]}
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"rewards": [], "tool_calls": []})))
# “全局平均 tool calls（按记录）”列表
global_tool_calls_by_group = defaultdict(lambda: defaultdict(list))  # [dataset][exp] -> [counts...]

def _sort_key(row: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    排序健壮键：
    1) 没 runid 的排在后面 (bool -> int：True=1, False=0)
    2) 其次按 order（缺 runid 时产生的自增序）
    3) 最后按 runid
    """
    no_runid = 1 if row.get("runid") is None else 0
    order = row.get("order") if row.get("order") is not None else 10**9
    runid = row.get("runid") if row.get("runid") is not None else 10**9
    return (no_runid, order, runid)

for pass_i_info in pass_1_infoes:
    dataset = pass_i_info['dataset']   # e.g. AIME24 / AIME25
    exp = pass_i_info['exp']           # 'y' 或 'n'

    # 先按 problem_hash 分桶收集，再排序
    bucket: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in pass_i_info['val_log']:
        bucket[row["problem_hash"]].append(row)
        # 全局记录级的 tool_calls 统计（按记录口径）
        global_tool_calls_by_group[dataset][exp].append(row["tool_calls"])

    for phash, rows in bucket.items():
        rows_sorted = sorted(rows, key=_sort_key)
        data[dataset][exp][phash]["rewards"].extend([r["reward"] for r in rows_sorted])
        data[dataset][exp][phash]["tool_calls"].extend([r["tool_calls"] for r in rows_sorted])

# 转普通 dict
data = {ds: {ex: dict(problems) for ex, problems in ex_dic.items()} for ds, ex_dic in data.items()}

# -------------------------------
# 计算指标
# -------------------------------
def _compute_metrics_at_k(samples_by_problem: Dict[str, Dict[str, List[float]]], k: int) -> Tuple[float, float, float]:
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

        if any(r > 0 for r in rw):
            pass_cnt += 1

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

def AIME_METRICS_k(data: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]], k: int) -> None:
    """
    打印 AIME24/AIME25 下 exp=y/n 的：
      - pass@k
      - mean_reward@k
      - mean_tool_calls@k（按题口径）
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

# -------------------------------
# 运行
# -------------------------------
if __name__ == "__main__":
    AIME_METRICS_k(data, 32)
