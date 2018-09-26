#!/usr/bin/env bash


K=30
input_dir=/Users/gegaojian/Desktop/GPU_outputs/news/
label_pt=/Users/gegaojian/PycharmProjects/final_experiment/news_input/subject_document_label.txt
output_dir=/Users/gegaojian/Desktop/gpu_scores/news/k${K}/

echo "================ Score ============="

for round in $(seq 1 1 10); do

echo "=============== Round : $round ============="
pzd_pt=${input_dir}${round}round_${K}topic_weight05_snippet_filter20_iter1000_gpudmm_pdz.txt
pwz_pt=${input_dir}${round}round_${K}topic_weight05_snippet_filter20_iter1000_gpudmm_phi.txt
dwid_pt=${input_dir}doc_wids.txt
python3 scores.py $pzd_pt $pwz_pt $dwid_pt $label_pt $K $output_dir

done

echo "================ Mean ============="
python3 mean.py $output_dir