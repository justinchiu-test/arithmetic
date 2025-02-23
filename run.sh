#!/bin/bash

do_generate=True
do_promptify=True
do_fewshot=True

#for i in 2 3 4 5
#for i in 3
for i in 3 5 7 9
do
    # training set of 100k
    #uv run python -m arithmetic.generate --num_examples 100000 --min_value 10_000 --max_value 1_000_000 --num_values $i --do_generate $do_generate --do_promptify $do_promptify --do_fewshot $do_fewshot
    # training set of 50k
    #uv run python -m arithmetic.generate --num_examples 50000 --min_value 10_000 --max_value 1_000_000 --num_values $i --do_generate $do_generate --do_promptify $do_promptify --do_fewshot $do_fewshot
    # training set of 20k
    uv run python -m arithmetic.generate --num_examples 20000 --min_value 10_000 --max_value 1_000_000 --num_values $i --do_generate $do_generate --do_promptify $do_promptify --do_fewshot $do_fewshot
    # test set of 10k
    uv run python -m arithmetic.generate --num_examples 10000 --min_value 10_000 --max_value 1_000_000 --num_values $i
done

