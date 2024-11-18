model_folder=/DATA/temp/auto_avsr
modality=video
pretrained_path=/DATA/temp/auto_avsr/train1207/cleaned.ckpt
mouthD=mouth
wavD=wav
csv_file=/home/aiv-gpu-019/trainAvsr.csv

python $model_folder/eval.py data.modality=$modality data.dataset.root_dir=/DATA/temp/auto_avsr data.dataset.test_file=$csv_file label_flag=1 mouth_dir=$mouthD wav_dir=$wavD pretrained_model_path=$pretrained_path 