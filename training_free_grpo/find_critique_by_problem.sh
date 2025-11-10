#!/bin/bash

# 定义源文件路径
SOURCE_FILE="/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_1/single_query_critique.jsonl"

# 定义目标输出目录
OUTPUT_DIR="/data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_1/SAMPLE_TO_RESEARCH"

# 要匹配的字符串（注意双引号和反斜杠需要正确转义）
TARGET_STRING='"problem": "Evaluate the expression:\n\\[2^{7} \\times 3^{0} + 2^{6} \\times 3^{1} + 2^{5} \\times 3^{2} + \\cdots + 2^{0} \\times 3^{7}.\\]",'

# 创建输出目录（如不存在则创建）
mkdir -p "$OUTPUT_DIR"

echo "开始扫描文件: $SOURCE_FILE"
echo "查找包含目标字段的行..."
echo "输出目录: $OUTPUT_DIR"

# 初始化计数器
MATCH_COUNT=0

# 逐行读取文件并查找目标字符串
LINE_NUM=0
while IFS= read -r LINE; do
    ((LINE_NUM++))
    if [[ "$LINE" == *"$TARGET_STRING"* ]]; then
        ((MATCH_COUNT++))
        OUTPUT_FILE="${OUTPUT_DIR}/match_${MATCH_COUNT}_line_${LINE_NUM}_critique.json"
        echo "$LINE" > "$OUTPUT_FILE"
        echo "  [匹配] 第 $LINE_NUM 行 -> $OUTPUT_FILE"
    fi
done < "$SOURCE_FILE"

if [ $MATCH_COUNT -eq 0 ]; then
    echo "未找到任何匹配项。"
else
    echo "共找到 $MATCH_COUNT 条匹配行，已全部保存到 $OUTPUT_DIR。"
fi
