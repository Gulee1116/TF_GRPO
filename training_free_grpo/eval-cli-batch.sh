# # AIME24
# bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 8 --experience_exist y
# bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 8 --experience_exist n

# # AIME25
# bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 8 --experience_exist y
# bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 8 --experience_exist n
    for i in {2..32}; do
        bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist n
        echo "done doing ${i}/32 eval AIME24 EXP N"
        bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 1 --experience_exist n
        echo "done doing ${i}/32 eval AIME25 EXP N"
        bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist y
        echo "done doing ${i}/32 eval AIME24 EXP y"
        bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 1 --experience_exist y
        echo "done doing ${i}/32 eval AIME25 EXP y"
    done
# # AIME24
#     # Mean@32
#     for i in {1..32}; do
#         bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist y
#         bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist n
#     done