#!/bin/bash

# 默认值
DATASET_NAME=""
PASS_K_VALUE=""
ROLLOUT_CONCURRENCY=128
EXPERIENCE_EXIST="" 

NONE_EXP_FILE_PATH=/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_3/experiences_NULL.json 
EXP_FILE_PATH=/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_3/experiences.json

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

usage() {
    echo "用法: $0 --dataset <名称> --pass_k <数值> --experience_exist <y|n> [选项]"
    echo ""
    echo "必选参数:"
    echo "  --dataset <名称>          指定数据集名称 (例如: AIME24)"
    echo "  --pass_k <数值>           指定 Pass@k 的数值 (例如: 8 或 32)"
    echo "  --experience_exist <y|n> 是否存在经验文件。"
    echo ""
    echo "可选参数:"
    echo "  --concurrency <数值>      指定并发数 (默认: 128)"
    echo "  -h, --help                显示此帮助信息"
}

# ----------------------------------------------
# 2. 解析长格式参数
# ----------------------------------------------

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dataset)
            DATASET_NAME="$2"
            shift 2
            ;;
        --pass_k)
            PASS_K_VALUE="$2"
            shift 2
            ;;
        --experience_exist)
            EXPERIENCE_EXIST="$2"
            shift 2
            ;;
        --concurrency)
            ROLLOUT_CONCURRENCY="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "错误：未知参数 '$1'" >&2
            usage
            exit 1
            ;;
    esac
done

# 验证核心必选参数
if [ -z "$DATASET_NAME" ] || [ -z "$PASS_K_VALUE" ] || [ -z "$EXPERIENCE_EXIST" ]; then
    echo "错误：必须指定 --dataset, --pass_k 和 --experience_exist 参数！" >&2
    usage
    exit 1
fi

# 验证 --experience_exist 的枚举值
if [[ "$EXPERIENCE_EXIST" != "y" && "$EXPERIENCE_EXIST" != "n" ]]; then
    echo "错误：--experience_exist 的值必须是 'y' 或 'n'。" >&2
    usage
    exit 1
fi

# 根据 --experience_exist 决定最终的 EXP_FILE_PATH
if [ "$EXPERIENCE_EXIST" == "y" ]; then
    EFFECTIVE_EXP_FILE=$EXP_FILE_PATH
else
    EFFECTIVE_EXP_FILE=$NONE_EXP_FILE_PATH
fi

# experiment_name
EXPERIMENT_NAME="${DATASET_NAME}_pass_${PASS_K_VALUE}_exp_${EXPERIENCE_EXIST}_${TIMESTAMP}_eval"


# -------- eval start
export PYTHONPATH=$PWD:$PYTHONPATH

RESULTS=$(python training_free_grpo/main.py \
    --mode agent \
    --domain math \
    --experiment_name "${EXPERIMENT_NAME}" \
    --dataset "${DATASET_NAME}" \
    --experience_file "${EFFECTIVE_EXP_FILE}" \
    --rollout_concurrency "${ROLLOUT_CONCURRENCY}" \
    --pass_k "${PASS_K_VALUE}"
    2>/dev/null)
mkdir -p training_free_grpo/eval_results/pass${PASS_K_VALUE}
echo -e "$RESULTS" | grep -E "^- " | tail -n 3 > "training_free_grpo/eval_results/pass${PASS_K_VALUE}/${EXPERIMENT_NAME}.txt"