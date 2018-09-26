#!/usr/bin/env bash

# output_dir=/Users/gegaojian/PycharmProjects/final_experiment/output/
output_dir=/Users/gegaojian/PycharmProjects/final_experiment/medical_output/
# 1.将训练语料Corpus合并到text8中
echo "=============== Merge Origin Corpus 2 Text8 ============="
corpus_pt=/Users/gegaojian/PycharmProjects/final_experiment/medical_input/spilit.txt
text8_pt=/Users/gegaojian/PycharmProjects/final_experiment/input/text8
new_text8_pt=${output_dir}text8
cp $text8_pt $output_dir
python3 merge_corpus2text8.py $corpus_pt $new_text8_pt


# 2.根据合并后的语料训练word2vec模型  =>  w2v.model
echo "=============== Train Word2Vec Model ============="
w2v_size=100
w2v_window=5
w2v_alpha=0.02
w2v_workers=4
w2v_min_count=0
w2v_iter=100
w2v_hs=1
w2v_sg=1
#w2v_corpus_pt=${corpus_pt}
w2v_corpus_pt=${output_dir}text8
 w2v_model_pt=${output_dir}w2v.model
#w2v_model_pt=/Users/gegaojian/Desktop/experiment/origin_corpus_tp_outputs/text8_size100_window5_alpha0.02_iter100_hs1_sg1.word2vec
#echo "word2vec训练语料:$w2v_corpus_pt"
echo "word2vec训练语料:$corpus_pt"
echo "word2vec模型输出:$w2v_model_pt"
echo "参数 size:$w2v_size window:$w2v_window alpha:$w2v_alpha workers:$w2v_workers min_count:$w2v_min_count iter:$w2v_iter hs:$w2v_hs sg:$w2v_sg"

python3 word2vec_wrapper.py $corpus_pt $w2v_model_pt $w2v_size $w2v_window $w2v_alpha $w2v_workers $w2v_min_count $w2v_iter $w2v_hs $w2v_sg


# 3.序列化Corpus并得到词汇表  =>  doc_wids.txt 和 voca.txt
echo "=============== Index Docs ============="
# docs after indexing
dwid_pt=${output_dir}doc_wids.txt
# vocabulary file
voca_pt=${output_dir}voca.txt

python3 indexDocs.py $corpus_pt $dwid_pt $voca_pt


# 4.根据 *.w2v 和 voca.txt 得到单词映射表并序列化  =>  mapped_wids.txt
echo "=============== Map Words Then Index ============="
# 前n个近义词
ntop=15
# 最小近义相似度阀值
threshold=0.9
wm_pt=${output_dir}words_map.txt
mw_pt=${output_dir}mapped_wids.txt

python3 map2index.py $w2v_model_pt $voca_pt $ntop $threshold $wm_pt $mw_pt


# 5.将 doc_wids.txt 、mapped_wids.txt 作为输入 训练 Gloss Model  =>  .pw_z .pz .pz_d
model_dir=${output_dir}model/
mkdir -p $output_dir/model

btm_K=200
btm_alpha=`echo "scale=3;50/$btm_K"|bc`
btm_beta=0.05
btm_niter=500
btm_save_step=501

for i in $(seq 1 1 10); do
# learning parameters p(z) and p(w|z)
echo "=============== Time : $i ============="
echo "=============== Topic Learning ============="
W=`wc -l < $voca_pt` # vocabulary size
gen_all=1
make -C ../src
echo "../src/btm est $btm_K $W $btm_alpha $btm_beta $btm_niter $btm_save_step $dwid_pt $mw_pt $gen_all $model_dir"
../src/btm est $btm_K $W $btm_alpha $btm_beta $btm_niter $btm_save_step $dwid_pt $mw_pt $gen_all $model_dir

# infer p(z|d) for each doc
echo "================ Infer P(z|d)==============="
echo "../src/btm inf sub_w $btm_K $dwid_pt $model_dir"
../src/btm inf sub_w $btm_K $dwid_pt $model_dir

## output top words of each topic
echo "================ Topic Display ============="
python3 topicDisplay.py $model_dir $btm_K $voca_pt

# 6.指标: coherence
echo "================ Score ============="
btm_pzd_pt=${model_dir}k${btm_K}.pz_d
btm_pwz_pt=${model_dir}k${btm_K}.pw_z
label_pt=/Users/gegaojian/PycharmProjects/final_experiment/medical_input/label.txt
python3 scores.py $btm_pzd_pt $btm_pwz_pt $dwid_pt $label_pt $btm_K $output_dir
done

echo "================ Mean ============="
python3 mean.py $output_dir