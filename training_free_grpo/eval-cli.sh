#!/bin/bash

# =========================
# 参数与默认值
# =========================
DATASET_NAME=""
PASS_K_VALUE=""
ROLLOUT_CONCURRENCY=128
EXPERIENCE_EXIST=""
EXP_INDEX=EXP1109

# EXP_FILE_PATH=/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_3/experiences.json
EXP_FILE_PATH=/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100_20251107/step_3/experiences.json
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

usage() {
    echo "用法: $0 --dataset <名称> --pass_k <数值> --experience_exist <y|n> [选项]"
    echo ""
    echo "必选参数:"
    echo "  --dataset <名称>          指定数据集名称 (例如: AIME24)"
    echo "  --pass_k <数值>           指定 Pass@k 的数值 (例如: 8 或 32)"
    echo "  --experience_exist <y|n>  是否存在经验文件。"
    echo ""
    echo "可选参数:"
    echo "  --concurrency <数值>      指定并发数 (默认: 128)"
    echo "  -h, --help                显示此帮助信息"
}

# =========================
# 参数解析
# =========================
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dataset) DATASET_NAME="$2"; shift 2 ;;
        --pass_k) PASS_K_VALUE="$2"; shift 2 ;;
        --experience_exist) EXPERIENCE_EXIST="$2"; shift 2 ;;
        --concurrency) ROLLOUT_CONCURRENCY="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "错误：未知参数 '$1'"; usage; exit 1 ;;
    esac
done

# =========================
# 参数校验
# =========================
if [ -z "$DATASET_NAME" ] || [ -z "$PASS_K_VALUE" ] || [ -z "$EXPERIENCE_EXIST" ]; then
    echo "错误：必须指定 --dataset, --pass_k 和 --experience_exist 参数！" >&2
    usage
    exit 1
fi

if [[ "$EXPERIENCE_EXIST" != "y" && "$EXPERIENCE_EXIST" != "n" ]]; then
    echo "错误：--experience_exist 的值必须是 'y' 或 'n'。" >&2
    usage
    exit 1
fi

# =========================
# 环境与变量
# =========================
EXPERIMENT_NAME="${DATASET_NAME}_pass_${PASS_K_VALUE}_exp_${EXPERIENCE_EXIST}_${TIMESTAMP}_eval"
export PYTHONPATH=$PWD:$PYTHONPATH

# =========================
# 构建命令
# =========================
CMD="python training_free_grpo/main.py \
    --mode agent \
    --domain math \
    --experiment_name \"${EXPERIMENT_NAME}\" \
    --dataset \"${DATASET_NAME}\" \
    --rollout_concurrency \"${ROLLOUT_CONCURRENCY}\" \
    --pass_k \"${PASS_K_VALUE}\""

if [ "$EXPERIENCE_EXIST" == "y" ]; then
    CMD="$CMD --experience_file \"${EXP_FILE_PATH}\""
fi

# =========================
# 打印命令并执行
# =========================
echo "🚀 运行命令如下："
echo "$CMD"
echo "---------------------------------------"

# 执行命令并捕获 stdout/stderr（不丢弃 stderr）
# 这样 RESULTS 中包含了所有输出，且 EXIT_CODE 保存实际退出码
RESULTS=$(eval "$CMD" 2>&1)
EXIT_CODE=$?
echo "---------------------------------------"
echo "✅ 命令执行完毕（退出码: $EXIT_CODE）"
echo ""

# =========================
# 结果保存
# =========================
mkdir -p training_free_grpo/eval_results/Qwen3-32B/${EXP_INDEX}/pass${PASS_K_VALUE}

# 保存全部日志
LOG_PATH="training_free_grpo/eval_results/Qwen3-32B/${EXP_INDEX}/pass${PASS_K_VALUE}/${EXPERIMENT_NAME}.log"
echo "$RESULTS" > "$LOG_PATH"

# 抽取关键统计行
echo "$RESULTS" | grep -E "^- " | tail -n 3 > "training_free_grpo/eval_results/Qwen3-32B/${EXP_INDEX}/pass${PASS_K_VALUE}/${EXPERIMENT_NAME}.txt"

echo "📄 结果摘要文件: training_free_grpo/eval_results/Qwen3-32B/${EXP_INDEX}/pass${PASS_K_VALUE}/${EXPERIMENT_NAME}.txt"
echo "🪵 完整日志文件: $LOG_PATH"
