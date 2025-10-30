# AIME24
    # Mean@32
    for i in {1..32}; do
        bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist y
        bash training_free_grpo/eval-cli.sh --dataset AIME24 --pass_k 1 --experience_exist n
    done

# AIME25
    # Mean@32
    for i in {1..32}; do
        bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 1 --experience_exist y
        bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 1 --experience_exist n
    done

    # Pass@8
    bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 8 --experience_exist y 
    bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 8 --experience_exist n

    # Pass@32
    bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 32 --experience_exist y
    bash training_free_grpo/eval-cli.sh --dataset AIME25 --pass_k 32 --experience_exist n
         
