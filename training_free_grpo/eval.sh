export PYTHONPATH=$PWD:$PYTHONPATH

python training_free_grpo/main.py \
    --mode agent \
    --domain math \
    --experiment_name AIME24_test_step_3_EXP_00_pass8_test \
    --dataset AIME24 \
    --rollout_concurrency 128 \
    --pass_k 1

    # --experience_file /data/wangziyue-20251013/training-free-grpo-data-dir/data/math/train/DAPO100/step_3/experiences.json \
